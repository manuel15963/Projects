document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const gridSize = 20;
    let snake = [{ x: gridSize * 5, y: gridSize * 5 }];
    let direction = { x: 0, y: 0 };
    let food = { x: gridSize * 10, y: gridSize * 10 };
    let gameInterval;

    canvas.width = 400;
    canvas.height = 400;

    function drawRect(x, y, color) {
        ctx.fillStyle = color;
        ctx.fillRect(x, y, gridSize, gridSize);
    }

    function moveSnake() {
        const head = { x: snake[0].x + direction.x, y: snake[0].y + direction.y };
        snake.unshift(head);

        if (head.x === food.x && head.y === food.y) {
            food = { x: gridSize * Math.floor(Math.random() * canvas.width / gridSize), y: gridSize * Math.floor(Math.random() * canvas.height / gridSize) };
        } else {
            snake.pop();
        }

        if (head.x < 0 || head.y < 0 || head.x >= canvas.width || head.y >= canvas.height || snake.slice(1).some(segment => segment.x === head.x && segment.y === head.y)) {
            clearInterval(gameInterval);
            alert("fin del juego mi king a casa nomas a Casa unistall please :v !");
        }
    }

    function drawGame() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        snake.forEach(segment => drawRect(segment.x, segment.y, "#2ecc71"));
        drawRect(food.x, food.y, "#e74c3c");
    }

    function gameLoop() {
        moveSnake();
        drawGame();
    }

    document.addEventListener("keydown", event => {
        switch (event.key) {
            case "ArrowUp":
                if (direction.y === 0) direction = { x: 0, y: -gridSize };
                break;
            case "ArrowDown":
                if (direction.y === 0) direction = { x: 0, y: gridSize };
                break;
            case "ArrowLeft":
                if (direction.x === 0) direction = { x: -gridSize, y: 0 };
                break;
            case "ArrowRight":
                if (direction.x === 0) direction = { x: gridSize, y: 0 };
                break;
        }
    });

    gameInterval = setInterval(gameLoop, 100);
});
