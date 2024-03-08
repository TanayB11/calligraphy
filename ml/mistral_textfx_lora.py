# https://www.databricks.com/blog/efficient-fine-tuning-lora-guide-llms

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from trl import SFTTrainer
from peft import LoraConfig, LoftQConfig, get_peft_model, PeftModel
from datasets import Dataset
import pandas as pd
import wandb

MAX_SEQ_LENGTH = 1024

wandb.init(
    project="calligraphy",
    # track hyperparameters and run metadata
    config={
        "architecture": "QLoRA",
        "dataset": "combined",
    }
)

# can change the quantization type using https://huggingface.co/blog/4bit-transformers-bitsandbytes
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = 'right'
tokenizer_function = lambda x : tokenizer(x['text'], truncation=True, padding='max_length', max_length=MAX_SEQ_LENGTH)

base_model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2", device_map='auto')

# load existing adapter (only if already exists!)
model = PeftModel.from_pretrained(base_model, 'models/mistral_similes/textfx_adapter')

# load dataset
train_dataset = Dataset.from_csv('./data/dataset_train.csv')
val_dataset = Dataset.from_csv('./data/dataset_val.csv')

tokenized_train_dataset = train_dataset.map(
    tokenizer_function,
    batched=True,
    num_proc=4
)

tokenized_val_dataset = val_dataset.map(
    tokenizer_function,
    batched=True,
    num_proc=4
)


# some LoRA hyperparameter config
loftq_config = LoftQConfig(loftq_bits=4)
lora_config = LoraConfig(
        r=16,
        lora_alpha=8,
        lora_dropout=0.05,
        task_type='CAUSAL_LM',
        init_lora_weights='loftq',
        loftq_config=loftq_config,
        target_modules=['q_proj', 'k_proj', 'v_proj', 'out_proj']
    )


model = get_peft_model(base_model, lora_config, adapter_name='textfx_adapter')
model.print_trainable_parameters()


# https://github.com/rajpurkar/cs197-lec4/blob/master/demo.ipynb
training_args = TrainingArguments(
    f'mistral_textfx',
    evaluation_strategy="epoch",
    logging_dir='./logs',
    learning_rate=2e-4,
    weight_decay=0.01,
    num_train_epochs=5,
    report_to='wandb'
)

trainer = SFTTrainer(
    model=model,
    train_dataset=tokenized_train_dataset,
    eval_dataset=tokenized_val_dataset,
    dataset_text_field='text',
    max_seq_length=MAX_SEQ_LENGTH,
    args=training_args
)

trainer.train()
trainer.model.save_pretrained(f'mistral_similes')
