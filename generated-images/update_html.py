import base64, io, os
from PIL import Image

# Define theme -> images mapping
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

# Process all images
output_lines = []
for theme_key, images in themes.items():
    arr_items = []
    for idx, (img_path, short) in enumerate(images):
        img = Image.open(img_path)
        img_resized = img.resize((500, 600), Image.LANCZOS)
        buf = io.BytesIO()
        if img_resized.mode == 'RGBA':
            img_resized = img_resized.convert('RGB')
        img_resized.save(buf, format='JPEG', quality=80, optimize=True)
        b64 = base64.b64encode(buf.getvalue()).decode()
        const_name = f"{theme_key}_{short}"
        output_lines.append(f"    const {const_name} = 'data:image/jpeg;base64,{b64}';")
        arr_items.append(const_name)
    
    arr_str = ', '.join(arr_items)
    output_lines.append(f"    const {theme_key}_IMGS = [{arr_str}];")

theme_block = '\n'.join(output_lines)

# Now read the HTML and replace
with open(r'D:\Documents\Workbuddy\2026-06-14-20-52-20\puzzle.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace theme constants section
start = html.find('// ===== Built-in Image Themes (base64 embedded) =====')
end = html.find('let currentTheme = 0;', start)

new_section = f"""    // ===== Built-in Image Theme Libraries (30 images total, 5 per theme) =====
{theme_block}
    let currentTheme = 0; // 0=手绘 1=动物 2=海洋 3=恐龙 4=太空 5=丛林
    let currentThemeImgIdx = 0; // which image within the current theme"""

html = html[:start] + new_section + html[end:]

# 2. Replace themeSources with themeLibs
html = html.replace(
    """    const themeSources = [
        null,                           // 0 = hand-drawn (generated by drawAnimalScene)
        THEME_USR1,                     // 1 = user animals
        THEME_USR2,                     // 2 = user ocean
        THEME_DINO,                     // 3 = dino
        THEME_SPACE,                    // 4 = space
        THEME_JUNGLE                    // 5 = jungle
    ];""",
    """    const THEME_COUNT = 6;
    const themeLibs = [
        null,           // 0 = hand-drawn (uses drawAnimalScene + THEME0_IMGS)
        THEME1_IMGS,    // 1 = 动物
        THEME2_IMGS,    // 2 = 海洋
        THEME3_IMGS,    // 3 = 恐龙
        THEME4_IMGS,    // 4 = 太空
        THEME5_IMGS     // 5 = 丛林
    ];"""
)

# 3. Replace generateTileImages
old_gen_func = """    function generateTileImages(themeIdx, callback) {
        const srcCanvas = document.createElement('canvas');
        srcCanvas.width = SOURCE_W;
        srcCanvas.height = SOURCE_H;
        const ctx = srcCanvas.getContext('2d');

        function finish() {
            previewImg.src = srcCanvas.toDataURL('image/png', 0.92);
            sliceTiles(srcCanvas);
            if (callback) callback();
        }

        if (themeIdx === 0 || !themeSources[themeIdx]) {
            // Draw the hand-drawn animal scene
            drawAnimalScene(ctx, SOURCE_W, SOURCE_H);
            finish();
        } else {
            // Load embedded image
            const img = new Image();
            img.onload = function() {
                ctx.drawImage(img, 0, 0, SOURCE_W, SOURCE_H);
                finish();
            };
            img.onerror = function() {
                // Fallback to hand-drawn
                drawAnimalScene(ctx, SOURCE_W, SOURCE_H);
                finish();
            };
            img.src = themeSources[themeIdx];
        }
    }"""

new_gen_func = """    function generateTileImages(themeIdx, imgIdx, callback) {
        const srcCanvas = document.createElement('canvas');
        srcCanvas.width = SOURCE_W;
        srcCanvas.height = SOURCE_H;
        const ctx = srcCanvas.getContext('2d');

        function finish() {
            previewImg.src = srcCanvas.toDataURL('image/png', 0.92);
            sliceTiles(srcCanvas);
            if (callback) callback();
        }

        function loadImg(url) {
            const img = new Image();
            img.onload = function() { ctx.drawImage(img, 0, 0, SOURCE_W, SOURCE_H); finish(); };
            img.onerror = function() { drawAnimalScene(ctx, SOURCE_W, SOURCE_H); finish(); };
            img.src = url;
        }

        if (themeIdx === 0) {
            if (imgIdx === 0) {
                drawAnimalScene(ctx, SOURCE_W, SOURCE_H);
                finish();
            } else if (THEME0_IMGS && THEME0_IMGS[imgIdx - 1]) {
                loadImg(THEME0_IMGS[imgIdx - 1]);
            } else {
                drawAnimalScene(ctx, SOURCE_W, SOURCE_H);
                finish();
            }
        } else if (themeLibs[themeIdx] && themeLibs[themeIdx][imgIdx]) {
            loadImg(themeLibs[themeIdx][imgIdx]);
        } else if (themeLibs[themeIdx] && themeLibs[themeIdx][0]) {
            loadImg(themeLibs[themeIdx][0]);
        } else {
            drawAnimalScene(ctx, SOURCE_W, SOURCE_H);
            finish();
        }
    }"""

html = html.replace(old_gen_func, new_gen_func)

# 4. Replace switchTheme
old_switch = """    function switchTheme(themeIdx) {
        if (themeIdx === currentTheme) return;
        stopConfetti();
        victoryOverlay.classList.remove('show');
        stopTimer();

        // Update active button
        themeSelector.querySelectorAll('.btn').forEach(btn => {
            btn.classList.toggle('active', parseInt(btn.dataset.theme) === themeIdx);
        });

        currentTheme = themeIdx;
        generateTileImages(themeIdx, function() {
            newGame();
        });
    }"""

new_switch = """    function switchTheme(themeIdx) {
        if (themeIdx === currentTheme) return;
        stopConfetti();
        victoryOverlay.classList.remove('show');
        stopTimer();

        themeSelector.querySelectorAll('.btn').forEach(btn => {
            btn.classList.toggle('active', parseInt(btn.dataset.theme) === themeIdx);
        });

        currentTheme = themeIdx;
        currentThemeImgIdx = 0;
        generateTileImages(themeIdx, 0, function() {
            initGame();
        });
    }"""

html = html.replace(old_switch, new_switch)

# 5. Replace newGame
old_newgame = """    function newGame() {
        stopConfetti();
        victoryOverlay.classList.remove('show');
        stopTimer();
        initGame();
    }"""

new_newgame = """    function newGame() {
        stopConfetti();
        victoryOverlay.classList.remove('show');
        stopTimer();

        if (isRunning) stopTimer();

        const maxIdx = (currentTheme === 0) ? THEME0_IMGS.length + 1 : themeLibs[currentTheme].length;
        currentThemeImgIdx = Math.floor(Math.random() * maxIdx);

        generateTileImages(currentTheme, currentThemeImgIdx, function() {
            initGame();
        });
    }"""

html = html.replace(old_newgame, new_newgame)

# 6. Replace bootstrap
html = html.replace(
    """    function bootstrap() {
        generateTileImages(0, function() {
            setupEvents();
            initGame();
        });
    }""",
    """    function bootstrap() {
        generateTileImages(0, 0, function() {
            setupEvents();
            initGame();
        });
    }"""
)

with open(r'D:\Documents\Workbuddy\2026-06-14-20-52-20\puzzle.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! HTML updated successfully.")
