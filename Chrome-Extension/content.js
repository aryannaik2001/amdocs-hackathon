document.addEventListener('mouseup', function() {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {
      // You can add right-click menu functionality here
      chrome.runtime.sendMessage({
        type: 'TEXT_SELECTED',
        text: selectedText
      });
    }
  });