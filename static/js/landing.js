// landing.js
// Renders a slow-moving network of connected nodes on the landing page,
// visually representing the idea of interconnected data points feeding
// a prediction model. Motion is deliberately slow and subtle.

const canvas = document.getElementById('networkCanvas');
const ctx = canvas.getContext('2d');

let width, height;
let nodes = [];

const NODE_COUNT = 42;
const LINK_DISTANCE = 130;
const ACCENT = '#4F8CFF';
const ACCENT_SOFT = 'rgba(79, 140, 255, 0.18)';

function resize() {
    width = canvas.width = canvas.offsetWidth;
    height = canvas.height = canvas.offsetHeight;
}

function initNodes() {
    nodes = Array.from({ length: NODE_COUNT }, () => ({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.25,
        vy: (Math.random() - 0.5) * 0.25,
        r: Math.random() * 1.6 + 1
    }));
}

function step() {
    ctx.clearRect(0, 0, width, height);

    // update positions
    for (const n of nodes) {
        n.x += n.vx;
        n.y += n.vy;
        if (n.x < 0 || n.x > width) n.vx *= -1;
        if (n.y < 0 || n.y > height) n.vy *= -1;
    }

    // draw links between nearby nodes
    for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
            const dx = nodes[i].x - nodes[j].x;
            const dy = nodes[i].y - nodes[j].y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < LINK_DISTANCE) {
                ctx.strokeStyle = ACCENT_SOFT;
                ctx.globalAlpha = 1 - dist / LINK_DISTANCE;
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(nodes[i].x, nodes[i].y);
                ctx.lineTo(nodes[j].x, nodes[j].y);
                ctx.stroke();
            }
        }
    }

    // draw nodes
    ctx.globalAlpha = 1;
    for (const n of nodes) {
        ctx.fillStyle = ACCENT;
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
        ctx.fill();
    }

    requestAnimationFrame(step);
}

window.addEventListener('resize', () => {
    resize();
    initNodes();
});

resize();
initNodes();
step();
