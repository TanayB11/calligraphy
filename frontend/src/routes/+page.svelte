<svelte:head>
  <link rel="stylesheet" href="https://unpkg.com/trix@2.0.8/dist/trix.css">
  <script src="https://unpkg.com/trix@2.0.8/dist/trix.umd.min.js"></script>
</svelte:head>

<script>
  import { writable } from 'svelte/store';

  let selection = ''
  let apiBaseUrl = 'http://localhost:8000/ml/' // TODO: change to env var

	// let promise = Promise.resolve([]); // TODO: rename
  let suggestions = writable([]);

  function handleSelection() {
    var element = document.querySelector("trix-editor")

    let range = element.editor.getSelectedRange();
    selection = element.editor.getDocument().getStringAtRange(range)
  }

  async function handleSuggestion(type) {
    const response = await fetch(apiBaseUrl + type + '/', {
      method: 'POST',
      mode: 'cors',
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 'prompt': selection })
    })

    if (response.ok) {
      let output = await response.json()
      let cardText = output.completion.text
      console.log(cardText)

      if (type != 'critique') {
        cardText = output.prompt + " " + cardText
      }

      suggestions.update(currentSuggestions => {
        return [...currentSuggestions, cardText]
      })
    } else {
      throw new Error();
    }
  }

  function deleteSuggestion(index) {
    suggestions.update(currentSuggestions => {
      return currentSuggestions.filter((_, i) => i !== index);
    });
  }
</script>


<main class="container">

  <h1>Calligraphy</h1>

  <div class="row">
    <div class="col">
      <trix-toolbar id="trix_toolbar"></trix-toolbar>
      <trix-editor id="writing_textarea" toolbar="trix_toolbar" on:trix-selection-change={handleSelection}></trix-editor>
    </div>
    <div class="col">
      <a class="button primary" on:click="{() => handleSuggestion('critique')}">Critique</a>
      <a class="button primary" on:click="{() => handleSuggestion('simile')}">Simile</a>
      <a class="button primary" on:click="{() => handleSuggestion('scene')}">Scene</a>
      <a class="button primary" on:click="{() => handleSuggestion('pov')}">POV</a>

      <div class="col">
        {#each $suggestions.slice().reverse() as suggestion, index}
          <div class="card suggestion">
            {#each suggestion.split('\n') as line}
              <p>{line}</p>
            {/each}
            <button on:click="{() => deleteSuggestion(index)}">Delete</button>
          </div>
        {/each}
      </div>
    </div>
  </div>
</main>

<style>
  main {
    max-width: 50%;
    margin: 0 auto;
    padding: 2rem;
  }

  #writing_textarea {
    border: 1px solid;
    /* height: 50rem; /* Set the fixed height */
    resize: none; /* Prevent resizing */
  }

  .suggestion {
    margin-top: 1rem;
    margin-bottom: 1rem;
  }
</style>
