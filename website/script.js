function init() {
async function loadCrosswordData() {
    try {
        const response = await fetch('crosswordData.json');
        const crosswordData = await response.json();
        createCrossword(crosswordData);
      } catch (error) {
        console.error("Error fetching crossword data:", error);
      }
    }
  
  function createCrossword(crosswordData) {
    function createEmptyGrid(width, height) {
      const grid = new Array(height);
      for (let i = 0; i < height; i++) {
        grid[i] = new Array(width).fill("_");
      }
      return grid;
    }
  
    function populateGrid(grid, data) {
      data.forEach(({ answer, startx, starty, orientation }) => {
        for (let i = 0; i < answer.length; i++) {
          if (orientation === "across") {
            grid[starty - 1][startx - 1 + i] = answer[i];
          } else {
            grid[starty - 1 + i][startx - 1] = answer[i];
          }
        }
      });
      return grid;
    }
  
    const crossword = document.getElementById("crossword");
    crossword.innerHTML = "";
    const gridWidth = 13;
    const gridHeight = 13;
    const grid = createEmptyGrid(gridWidth, gridHeight);
    const populatedGrid = populateGrid(grid, crosswordData);
  
    crossword.style.gridTemplateColumns = `repeat(${gridWidth}, 30px)`; // Add this line to fix the grid layout
  
    populatedGrid.forEach((row, rowIndex) => {
        row.forEach((cell, cellIndex) => {
          const crosswordCell = document.createElement("div");
          crosswordCell.classList.add("cell");
          if (cell === "_") {
            crosswordCell.classList.add("cell-black"); // Add this line to apply the black background
          }
          crosswordCell.id = `cell-${rowIndex}-${cellIndex}`;
          crosswordCell.textContent = cell !== "_" ? cell : "";
          crossword.appendChild(crosswordCell);
        });
      });
      
  
    // Display clues
    const cluesAcross = crosswordData.filter(({ orientation }) => orientation === "across");
    const cluesDown = crosswordData.filter(({ orientation }) => orientation === "down");
  
    const cluesElement = document.getElementById("clues");
    cluesElement.innerHTML = "";
    const cluesAcrossElement = document.createElement("div");
    cluesAcrossElement.innerHTML = "<h3>Across:</h3>" + cluesAcross.map(({ position, clue }) => `<div><strong>${position}.</strong> ${clue}</div>`).join("");
    cluesElement.appendChild(cluesAcrossElement);
  
    const cluesDownElement = document.createElement("div");
    cluesDownElement.innerHTML = "<h3>Down:</h3>" + cluesDown.map(({ position, clue }) => `<div><strong>${position}.</strong> ${clue}</div>`).join('');
    cluesElement.appendChild(cluesDownElement);
  }
  
  loadCrosswordData();
  
}

init()

setInterval(() => {
    init();
}, 5000);