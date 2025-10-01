const lyricsContainer = document.getElementById('lyrics-container');

// You can tweak this value! If lyrics are still too fast, make it bigger (e.g., 700).
// If lyrics are too slow, make it smaller (e.g., 300).
const SYNC_OFFSET_MS = 575;


let currentLyrics = '';
let parsedLyrics = [];
let currentLineIndex = -1;

function parseLRC(lrcText) {
    const lines = lrcText.split('\n');
    const parsed = [];
    const timeRegex = /\[(\d{2}):(\d{2})\.(\d{2,3})\]/;

    for (const line of lines) {
        const match = line.match(timeRegex);
        if (match) {
            const minutes = parseInt(match[1], 10);
            const seconds = parseInt(match[2], 10);
            const milliseconds = parseInt(match[3].padEnd(3, '0'), 10); 
            const time = (minutes * 60 * 1000) + (seconds * 1000) + milliseconds;
            const text = line.replace(timeRegex, '').trim();
            if (text) {
                parsed.push({ time, text });
            }
        }
    }
    return parsed;
}

async function updateLyrics() {
    try {
        const response = await fetch('/get_lyrics');
        const data = await response.json();

        if (data.lyrics !== currentLyrics) {
            currentLyrics = data.lyrics;
            parsedLyrics = parseLRC(currentLyrics);
            currentLineIndex = -1; 
            lyricsContainer.innerHTML = '';
            if (parsedLyrics.length > 0) {
                parsedLyrics.forEach((line, index) => {
                    const li = document.createElement('li');
                    li.id = `line-${index}`;
                    li.textContent = line.text;
                    lyricsContainer.appendChild(li);
                });
            } else {
                const li = document.createElement('li');
                li.textContent = currentLyrics;
                lyricsContainer.appendChild(li);
            }
        }

        if (parsedLyrics.length > 0) {
            const compensatedProgress = data.progress_ms + SYNC_OFFSET_MS;

            let newCurrentLineIndex = -1;
            for (let i = 0; i < parsedLyrics.length; i++) {
                if (compensatedProgress >= parsedLyrics[i].time) {
                    newCurrentLineIndex = i;
                } else {
                    break;
                }
            }

            if (newCurrentLineIndex !== currentLineIndex) {
                if (currentLineIndex !== -1) {
                    const oldLine = document.getElementById(`line-${currentLineIndex}`);
                    if (oldLine) oldLine.classList.remove('active-line');
                }
                if (newCurrentLineIndex !== -1) {
                    const activeLineElement = document.getElementById(`line-${newCurrentLineIndex}`);
                    if (activeLineElement) {
                         activeLineElement.classList.add('active-line');
                        activeLineElement.scrollIntoView({
                            behavior: 'smooth',
                            block: 'center'
                        });
                    }
                }
                currentLineIndex = newCurrentLineIndex;
            }
        }

    } catch (error) {
        console.error('Error fetching lyrics:', error);
    }
}

updateLyrics();
setInterval(updateLyrics, 500);
