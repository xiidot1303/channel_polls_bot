webApp = Telegram.WebApp;
webApp.expand();
const bg = document.getElementById("bg");
const piece = document.getElementById("piece");
const slider = document.getElementById("slider");

const bgCtx = bg.getContext("2d");
const pieceCtx = piece.getContext("2d");

// ===== CONSTANTS =====
const WIDTH = 300;
const HEIGHT = 150;
const PIECE_SIZE = 40;
const TOLERANCE = 6;

// Piece starts slightly inside
const PIECE_START_X = 30;

// Hole more centered (not edge)
const HOLE_MIN_X = 150;
const HOLE_MAX_X = 210;

// ===== CANVAS SIZE =====
bg.width = piece.width = WIDTH;
bg.height = piece.height = HEIGHT;

// ===== RANDOM IMAGE =====
const images = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg"];
const bgImage = images[Math.floor(Math.random() * images.length)];

const img = new Image();
img.src = `/static/captcha/images/${bgImage}`;

// ===== TARGET POSITION =====
const targetX =
  Math.floor(Math.random() * (HOLE_MAX_X - HOLE_MIN_X)) + HOLE_MIN_X;

const targetY = Math.floor((HEIGHT - PIECE_SIZE) / 2);

// ===== DRAW =====
img.onload = () => {
  // Background
  bgCtx.clearRect(0, 0, WIDTH, HEIGHT);
  bgCtx.drawImage(img, 0, 0, WIDTH, HEIGHT);

  // Hole
  bgCtx.clearRect(targetX, targetY, PIECE_SIZE, PIECE_SIZE);

  bgCtx.strokeStyle = "rgba(255,255,255,0.6)";
  bgCtx.lineWidth = 2;
  bgCtx.strokeRect(targetX, targetY, PIECE_SIZE, PIECE_SIZE);

  // Puzzle piece (DRAW AT X = 0)
  pieceCtx.clearRect(0, 0, WIDTH, HEIGHT);
  pieceCtx.shadowColor = "rgba(0,0,0,0.35)";
  pieceCtx.shadowBlur = 8;

  pieceCtx.drawImage(
    img,
    targetX,
    targetY,
    PIECE_SIZE,
    PIECE_SIZE,
    0,
    targetY,
    PIECE_SIZE,
    PIECE_SIZE
  );

  // Reset position
  piece.style.left = PIECE_START_X + "px";
};

// ===== SLIDER =====
slider.min = PIECE_START_X;
slider.max = WIDTH - PIECE_SIZE - 10;
slider.value = PIECE_START_X;

// ===== MOVE =====
slider.addEventListener("input", () => {
  piece.style.left = slider.value + "px";
});

// ===== VERIFY =====
slider.addEventListener("change", () => {
  const pieceX = parseInt(slider.value);
  const diff = Math.abs(pieceX - targetX);
  webApp = Telegram.WebApp;
  webApp.expand();
  if (diff <= TOLERANCE) {
    Telegram.WebApp.sendData(
      JSON.stringify({
        captcha: "passed",
      })
    );
    webApp.close();
    // Telegram.WebApp.sendData("passed");
  } else {
    slider.value = PIECE_START_X;
    piece.style.left = PIECE_START_X + "px";
    alert("❌ Try again");
  }
});
