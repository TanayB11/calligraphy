<svelte:head>
  <link rel="stylesheet" href="https://unpkg.com/trix@2.0.8/dist/trix.css">
  <script src="https://unpkg.com/trix@2.0.8/dist/trix.umd.min.js"></script>
</svelte:head>

<script>
  let selection = '';

  // TODO: add handler for selected text:
  // 1. clean up HTML, only provide text
  // 2. show modal
  // 3. make API call to backend

  function handleSelection() {
    var element = document.querySelector("trix-editor")

    let range = element.editor.getSelectedRange();
    selection = element.editor.getDocument().getStringAtRange(range)
    console.log(selection)
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
      <form method="POST">
        <a class="button primary">Critique</a>
        <a class="button primary">Simile</a>
        <a class="button primary">Scene</a>
      </form>
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
    height: 50rem; /* Set the fixed height */
    resize: none; /* Prevent resizing */
  }
</style>
