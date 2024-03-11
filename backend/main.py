from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llama_cpp import Llama

llm = Llama(
    model_path='../ml/models/mistral_similes-Q5_K_S.gguf',
    chat_format="mistral-instruct",
    n_ctx=8192,
    n_gpu_layers=-1,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


class Prompt(BaseModel):
    prompt: str


@app.post("/ml/simile/")
async def gen_simile(prompt: Prompt):
    pre_prompt = """
        Create ONE simile that illustrates this concept: 
    """
    completion = llm.create_completion(
        pre_prompt + prompt.prompt, max_tokens=512, temperature=0.5
    )
    return {"prompt": prompt.prompt, "completion": completion["choices"][0]}


@app.post("/ml/fuse/")
async def gen_fuse(prompt: Prompt):
    pre_prompt = """
        Give a connection between the following two things, where the connection is novel and unexpected, rather than an unoriginal technicality: 
    """
    completion = llm.create_completion(
        pre_prompt + prompt.prompt, max_tokens=512, temperature=0.5
    )
    return {"prompt": prompt.prompt, "completion": completion["choices"][0]}


@app.post("/ml/pov/")
async def gen_pov(prompt: Prompt):
    pre_prompt = """
        A "hot take" is a perspective that is novel and thought-provoking. Give a hot take about 
    """
    completion = llm.create_completion(
        pre_prompt + prompt.prompt, max_tokens=512, temperature=0.5
    )
    return {"prompt": prompt.prompt, "completion": completion["choices"][0]}


@app.post("/ml/scene/")
async def gen_scene(prompt: Prompt):
    pre_prompt = """
        Sensory details are details that appeal to the five senses: vision, hearing, touch, smell, and taste. Sensory details make our writing more interesting and vivid, and the most effective sensory details are ones that are creative yet concrete and evocative. Provide a list of sensory details that evoke this thing: 
    """
    completion = llm.create_completion(
        pre_prompt + prompt.prompt, max_tokens=512, temperature=0.5
    )
    return {"prompt": prompt.prompt, "completion": completion["choices"][0]}


@app.post("/ml/explode/")
async def gen_explode(prompt: Prompt):
    pre_prompt = """
        A same-sounding phrase is a phrase that sounds like another word or phrase. Here is a same-sounding phrase for the word 
    """
    completion = llm.create_completion(
        pre_prompt + prompt.prompt, max_tokens=512, temperature=0.5
    )
    return {"prompt": prompt.prompt, "completion": completion["choices"][0]}


@app.post("/ml/critique/")
async def gen_critique(prompt: Prompt):
<<<<<<< Updated upstream
    pre_prompt = """
=======
    # https://www.reddit.com/r/ChatGPTPro/comments/14f6jqu/advanced_cot_prompts_for_gpt4_critical_ethical/
    pre_prompt = '''
>>>>>>> Stashed changes
        You are an advanced AI Language Model trained in persuasive writing, expository writing, and storytelling.
        Your task is to critique writing to the best of your ability.
        To ensure engaging and imaginative feedback, consider various writing elements and follow a step-by-step process.
        Reflect on each step and provide brief feedback.

        Now, let's work this out step by step to ensure we have a captivating and well-developed story:

            First, determine what type of piece this is.

            Make sure all descriptions are vivid and detailed.

            Reflect on the initial draft, identifying any areas for improvement or potential issues with argumentation, pacing, character development, or consistency.

            Critique sentence variety and diversity in vocabulary. Make sure the writing is clear and engaging.

            Point out which parts might need additional sources or fact-checking.

        Using this format, go ahead and create a well-crafted critique to the following writing:
    """
    completion = llm.create_completion(
        pre_prompt + prompt.prompt, max_tokens=4096, temperature=0.5
    )
    return {"prompt": prompt.prompt, "completion": completion["choices"][0]}
