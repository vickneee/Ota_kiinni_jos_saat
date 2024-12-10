// Initiate the sound when the page is loaded
window.addEventListener('load', function() {
  const audio = document.getElementById('celebration-audio');
  audio.muted = false;
  audio.play();
});