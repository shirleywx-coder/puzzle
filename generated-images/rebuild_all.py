import base64, io, math
from PIL import Image

HTML_PATH = r'D:\Documents\Workbuddy\2026-06-14-20-52-20\puzzle.html'

# ===== 1. Re-process images with watermark removed =====
# Map of theme -> image files (same as before, just re-processing)
themes = {
    'THEME0': [
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_animals_on_green__2026-06-20T14-17-51.png', 'H1'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_animal_picnic_sce_2026-06-20T14-18-53.png', 'H2'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_animals_having_fu_2026-06-20T14-19-22.png', 'H3'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_animals_going_to__2026-06-20T14-19-51.png', 'H4'),
    ],
    'THEME1': [
        (r'C:\Users\shirleywx\.workbuddy\clipboard-images\clipboard-2026-06-14T13-58-30-036Z-cc7261f9.jpg', 'A1'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_farm_animals_scen_2026-06-14T13-33-54.png', 'A2'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_animals_at_a_zoo__2026-06-20T14-26-35.png', 'A3'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_animals_with_babi_2026-06-20T14-27-01.png', 'A4'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_animals_in_winter_2026-06-20T14-27-35.png', 'A5'),
    ],
    'THEME2': [
        (r'C:\Users\shirleywx\.workbuddy\clipboard-images\clipboard-2026-06-14T13-58-30-043Z-7ca60b51.jpg', 'O1'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_ocean_sea_animals_2026-06-14T13-34-19.png', 'O2'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_ocean_underwater__2026-06-20T14-20-52.png', 'O3'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_ocean_scene__fish_2026-06-20T14-21-19.png', 'O4'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_ocean_beach_scene_2026-06-20T14-22-42.png', 'O5'),
    ],
    'THEME3': [
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_dinosaur_world__c_2026-06-14T14-03-57.png', 'D1'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_dinosaurs_scene___2026-06-20T14-20-18.png', 'D2'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_dinosaur_valley___2026-06-20T14-23-08.png', 'D3'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_dinosaurs_playing_2026-06-20T14-23-33.png', 'D4'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_dinosaurs_at_the__2026-06-20T14-23-59.png', 'D5'),
    ],
    'THEME4': [
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_space_adventure___2026-06-14T14-04-25.png', 'S1'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_space_planet_scen_2026-06-20T14-22-11.png', 'S2'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_space_station__co_2026-06-20T14-24-26.png', 'S3'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_space_alien_plane_2026-06-20T14-24-52.png', 'S4'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_space_solar_syste_2026-06-20T14-25-17.png', 'S5'),
    ],
    'THEME5': [
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_jungle_safari__co_2026-06-14T14-04-52.png', 'J1'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_forest_animals_sc_2026-06-14T13-34-45.png', 'J2'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_safari_jungle_ani_2026-06-20T14-21-45.png', 'J3'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_jungle_river_scen_2026-06-20T14-25-43.png', 'J4'),
        (r'D:\Documents\Workbuddy\2026-06-14-20-52-20\generated-images\Cute_cartoon_jungle_forest_flo_2026-06-20T14-26-09.png', 'J5'),
    ],
}

# Process: detect aspect ratio (1:1 -> 6x6, 5:6 -> 5x6), resize accordingly
# For square images: resize to 600x600 (6x6 grid)
# For portrait 5:6 images: resize to 500x600 (5x6 grid)
# Store the target grid size per image

def detect_grid(w, h):
    ratio = w / h
    if abs(ratio - 1.0) < 0.15:
        return (6, 6, 600, 600)
    else:
        return (5, 6, 500, 600)

output_lines = []
for theme_key, images in themes.items():
    arr_items = []
    for idx, (img_path, short) in enumerate(images):
        img = Image.open(img_path)
        iw, ih = img.size
        
        # Detect aspect ratio to determine target resize
        cols, rows, tw, th = detect_grid(iw, ih)
        img_resized = img.resize((tw, th), Image.LANCZOS)
        
        if img_resized.mode == 'RGBA':
            img_resized = img_resized.convert('RGB')
        
        buf = io.BytesIO()
        img_resized.save(buf, format='JPEG', quality=80, optimize=True)
        b64 = base64.b64encode(buf.getvalue()).decode()
        
        const_name = f"{theme_key}_{short}"
        output_lines.append(f"    const {const_name} = 'data:image/jpeg;base64,{b64}';")
        arr_items.append(const_name)
        shape = "6x6" if cols == 6 else "5x6"
        print(f"  {const_name}: {shape} {tw}x{th} {len(b64)//1024}KB")
    
    arr_str = ', '.join(arr_items)
    output_lines.append(f"    const {theme_key}_IMGS = [{arr_str}];")

theme_block = '\n'.join(output_lines)

# ===== 2. Now update the HTML =====
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# 2a. Replace theme constants section
start = html.find('// ===== Built-in Image Theme Libraries')
end = html.find('let currentTheme = 0;', start)

if start < 0 or end < 0:
    print("ERROR: theme markers not found!")
    exit()

new_section = f"""    // ===== Built-in Image Theme Libraries (30 images total, 5 per theme) =====
{theme_block}
    let currentThemeImgIdx = 0; // which image within the current theme
    let currentTheme = 0; // 0=手绘 1=动物 2=海洋 3=恐龙 4=太空 5=丛林"""

html = html[:start] + new_section + html[end:]

# 2b. Replace static constants with dynamic
old_consts = """    const ROWS = 6, COLS = 5, TOTAL = 30;
    const SOURCE_W = 500, SOURCE_H = 600;"""

new_consts = """    // Dynamic grid: detected from image aspect ratio
    let gridCols = 5, gridRows = 6, gridTotal = 30;
    let SRC_W = 500, SRC_H = 600;

    // Detect grid size from image aspect ratio
    function detectGridSize(w, h) {
        const ratio = w / h;
        if (Math.abs(ratio - 1.0) < 0.15) {
            return { cols: 6, rows: 6, sw: 600, sh: 600 };
        } else {
            return { cols: 5, rows: 6, sw: 500, sh: 600 };
        }
    }

    function applyGridSize(gs) {
        gridCols = gs.cols;
        gridRows = gs.rows;
        gridTotal = gs.cols * gs.rows;
        SRC_W = gs.sw;
        SRC_H = gs.sh;
        // Update CSS grid
        const grid = document.querySelector('.grid');
        if (grid) {
            grid.style.gridTemplateColumns = 'repeat(' + gridCols + ', 1fr)';
            grid.style.gridTemplateRows = 'repeat(' + gridRows + ', 1fr)';
        }
    }"""

html = html.replace(old_consts, new_consts)

# 2c. Replace ALL references to COLS, ROWS, TOTAL, SOURCE_W, SOURCE_H
# But be careful not to replace the function parameter names or CSS content
replacements = [
    ('(COLS)', '(gridCols)'),
    ('(ROWS)', '(gridRows)'),
    ('(TOTAL)', '(gridTotal)'),
    (' SOURCE_W', ' SRC_W'),
    (' SOURCE_H', ' SRC_H'),
    ('/ COLS;', '/ gridCols;'),
    ('/ ROWS;', '/ gridRows;'),
    ('% COLS;', '% gridCols;'),
    ('/ COLS ', '/ gridCols '),
    ('/ ROWS ', '/ gridRows '),
    ('i < TOTAL;', 'i < gridTotal;'),
    ('new Array(TOTAL)', 'new Array(gridTotal)'),
    ('length: TOTAL}', 'length: gridTotal}'),
    ('TOTAL - correct', 'gridTotal - correct'),
    ('SOURCE_W / SOURCE_H', 'SRC_W / SRC_H'),
]

for old, new in replacements:
    html = html.replace(old, new)

# 2d. Update generateTileImages to detect grid size from image
# The key change: when we load an image, first detect its grid size, then apply
old_gen = """    function generateTileImages(themeIdx, imgIdx, callback) {
        const srcCanvas = document.createElement('canvas');
        srcCanvas.width = SRC_W;
        srcCanvas.height = SRC_H;
        const ctx = srcCanvas.getContext('2d');

        function finish() {
            previewImg.src = srcCanvas.toDataURL('image/png', 0.92);
            sliceTiles(srcCanvas);
            if (callback) callback();
        }

        function loadImg(url) {
            const img = new Image();
            img.onload = function() { ctx.drawImage(img, 0, 0, SRC_W, SRC_H); finish(); };
            img.onerror = function() { drawAnimalScene(ctx, SRC_W, SRC_H); finish(); };
            img.src = url;
        }

        if (themeIdx === 0) {
            if (imgIdx === 0) {
                drawAnimalScene(ctx, SRC_W, SRC_H);
                finish();
            } else if (THEME0_IMGS && THEME0_IMGS[imgIdx - 1]) {
                loadImg(THEME0_IMGS[imgIdx - 1]);
            } else {
                drawAnimalScene(ctx, SRC_W, SRC_H);
                finish();
            }
        } else if (themeLibs[themeIdx] && themeLibs[themeIdx][imgIdx]) {
            loadImg(themeLibs[themeIdx][imgIdx]);
        } else if (themeLibs[themeIdx] && themeLibs[themeIdx][0]) {
            loadImg(themeLibs[themeIdx][0]);
        } else {
            drawAnimalScene(ctx, SRC_W, SRC_H);
            finish();
        }
    }"""

new_gen = """    function generateTileImages(themeIdx, imgIdx, callback) {
        // Step 1: determine the image URL and detect its grid size
        function finishWithImage(imgUrl) {
            const img = new Image();
            img.onload = function() {
                // Detect grid size from the actual image
                const gs = detectGridSize(img.naturalWidth, img.naturalHeight);
                applyGridSize(gs);
                
                const srcCanvas = document.createElement('canvas');
                srcCanvas.width = SRC_W;
                srcCanvas.height = SRC_H;
                const ctx = srcCanvas.getContext('2d');
                ctx.drawImage(img, 0, 0, SRC_W, SRC_H);
                
                previewImg.src = srcCanvas.toDataURL('image/png', 0.92);
                sliceTiles(srcCanvas);
                if (callback) callback();
            };
            img.onerror = function() { fallbackHandDrawn(); };
            img.src = imgUrl;
        }
        
        function fallbackHandDrawn() {
            // Use default 5x6 grid for hand-drawn scene
            const gs = { cols: 5, rows: 6, sw: 500, sh: 600 };
            applyGridSize(gs);
            const srcCanvas = document.createElement('canvas');
            srcCanvas.width = SRC_W;
            srcCanvas.height = SRC_H;
            const ctx = srcCanvas.getContext('2d');
            drawAnimalScene(ctx, SRC_W, SRC_H);
            previewImg.src = srcCanvas.toDataURL('image/png', 0.92);
            sliceTiles(srcCanvas);
            if (callback) callback();
        }

        if (themeIdx === 0) {
            if (imgIdx === 0) {
                fallbackHandDrawn();
            } else if (THEME0_IMGS && THEME0_IMGS[imgIdx - 1]) {
                finishWithImage(THEME0_IMGS[imgIdx - 1]);
            } else {
                fallbackHandDrawn();
            }
        } else if (themeLibs[themeIdx] && themeLibs[themeIdx][imgIdx]) {
            finishWithImage(themeLibs[themeIdx][imgIdx]);
        } else if (themeLibs[themeIdx] && themeLibs[themeIdx][0]) {
            finishWithImage(themeLibs[themeIdx][0]);
        } else {
            fallbackHandDrawn();
        }
    }"""

html = html.replace(old_gen, new_gen)

# 2e. Update sliceTiles to use dynamic grid vars
html = html.replace(
    'function sliceTiles(srcCanvas) {\n        const tw = SRC_W / gridCols;\n        const th = SRC_H / gridRows;\n        tileUrls = [];\n        for (let i = 0; i < gridTotal; i++) {\n            const col = i % gridCols;\n            const row = Math.floor(i / gridCols);',
    'function sliceTiles(srcCanvas) {\n        const tw = SRC_W / gridCols;\n        const th = SRC_H / gridRows;\n        tileUrls = [];\n        const total = gridCols * gridRows;\n        for (let i = 0; i < total; i++) {\n            const col = i % gridCols;\n            const row = Math.floor(i / gridCols);'
)

# 2f. Update fitGridToScreen
html = html.replace(
    '        const tileFromWidth = (maxGridContentWidth - gap) / gridCols;\n        const tileFromHeight = (maxGridContentHeight - gap) / gridRows;\n        gridTileSize = Math.floor(Math.min(tileFromWidth, tileFromHeight));',
    '        const tileFromWidth = (maxGridContentWidth - gap) / gridCols;\n        const tileFromHeight = (maxGridContentHeight - gap) / gridRows;\n        gridTileSize = Math.floor(Math.min(tileFromWidth, tileFromHeight));'
)

# 2g. Fix PRE_PLACED to be percentage-based
html = html.replace(
    '    const PRE_PLACED = 9;',
    '    const PRE_PLACED_RATIO = 0.3; // ~30% of total tiles'
)

# 2h. Update initGame to use PRE_PLACED_RATIO
html = html.replace(
    'const allPos = Array.from({length: gridTotal}, (_, i) => i);\n        shuffleArray(allPos);\n        const prePositions = allPos.slice(0, PRE_PLACED);',
    'const prePlacedCount = Math.floor(gridTotal * PRE_PLACED_RATIO);\n        const allPos = Array.from({length: gridTotal}, (_, i) => i);\n        shuffleArray(allPos);\n        const prePositions = allPos.slice(0, prePlacedCount);'
)

# 2i. Update the renderGrid CSS grid issue - it needs dynamic template
# The CSS currently uses grid-template-columns: repeat(5, 1fr) and grid-template-rows: repeat(6, 1fr)
# These need to be set via JS in applyGridSize, which we already added
# But the CSS file still has static values - need to remove them from CSS
css_old_grid = """        .grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            grid-template-rows: repeat(6, 1fr);
            gap: 2px;
        }"""

css_new_grid = """        .grid {
            display: grid;
            gap: 2px;
        }"""

html = html.replace(css_old_grid, css_new_grid)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print("\nDone! All updates complete.")
