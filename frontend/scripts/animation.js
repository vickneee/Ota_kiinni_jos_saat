export async function playVideoWithAnimation() {
  const videoContainer = document.getElementById('video-container');
  const video = document.getElementById('animation-video');

  // Show and animate the video container (rising up)
  videoContainer.style.display = 'block';
  videoContainer.classList.add('active'); // Add rising animation
  video.play();

  // Wait for the video to finish
  await new Promise((resolve) => {
    video.onended = () => {
      // Add the exit animation
      videoContainer.classList.remove('active');
      videoContainer.classList.add('exit'); // Start falling animation

      // Wait for the animation to complete
      setTimeout(() => {
        videoContainer.classList.remove('exit'); // Clean up the exit class
        videoContainer.style.display = 'none'; // Hide the video
        resolve(); // Resolve the promise after animation
      }, 1500); // Match this duration to the CSS transition time (1.5s)
    };
  });
}