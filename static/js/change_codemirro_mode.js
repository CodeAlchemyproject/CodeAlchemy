//C:text/x-csrc C++:text/x-c++src Python:python Java:text/x-java
var editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
    lineNumbers: true,
    indentUnit: 4,
    // Initial mode (assuming C by default)
    mode: 'text/x-csrc'
  });
  
  // Get the dropdown menu element
  var languageMenu = document.querySelector('.dropdown-menu');
  
  // Attach event listeners to dropdown items
  languageMenu.querySelectorAll('a.dropdown-item').forEach(function(item) {
    item.addEventListener('click', function(event) {
      event.preventDefault(); // Prevent default link behavior
  
      // Get the selected mode from the data-mode attribute
      var selectedMode = item.dataset.mode;
  
      // Update the editor's mode
      editor.setOption('mode', selectedMode);
    });
  });