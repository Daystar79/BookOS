#!/usr/bin/env bash
# Midlayer Build & Sync Script
# --------------------------
# 1. Pulls the latest core framework files from the CognitiveMiddleware.
# 2. Assembles draft chapters into Drafts/master_manuscript.md.
# 3. Compiles KDP print PDFs, DOCX manuscripts, and EPUB ebooks.

set -euo pipefail

# Path resolution
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORD_DIR="$ROOT/Build"
BUILD_DIR="$ROOT/Releases"
VENV_PYTHON="python3"
if [[ -d "$ROOT/.venv-docx" ]] && [[ -f "$ROOT/.venv-docx/bin/python" ]]; then
  VENV_PYTHON="$ROOT/.venv-docx/bin/python"
fi
MD_TO_DOCX="$WORD_DIR/md_to_docx.py"
EPUB_CSS="$WORD_DIR/epub.css"

# Step 1: Pull framework to keep in sync
echo "=== Step 1: Syncing Framework from CognitiveMiddleware ==="
"$VENV_PYTHON" "$ROOT/Build/pull_framework.py"

# Step 2: Assemble chapter drafts into master manuscript
echo -e "\n=== Step 2: Assembling Master Manuscript ==="
mkdir -p "$BUILD_DIR"

# Concatenate all draft chapters in natural sorted order if they exist
count=0
if ls "$ROOT/Drafts"/draft_chapter_*.md 1>/dev/null 2>&1; then
  rm -f "$ROOT/Drafts/master_manuscript.md"
  for f in $(find "$ROOT/Drafts" -maxdepth 1 -name "draft_chapter_*.md" | sort -V); do
    echo "  Integrating $(basename "$f")..."
    cat "$f" >> "$ROOT/Drafts/master_manuscript.md"
    echo -e "\n\n" >> "$ROOT/Drafts/master_manuscript.md"
    count=$((count+1))
  done
  echo "✓ Combined $count chapter(s) into Drafts/master_manuscript.md"
else
  if [[ -f "$ROOT/Drafts/master_manuscript.md" ]]; then
    echo "Using existing Drafts/master_manuscript.md"
  else
    echo "No draft files found in 'Drafts/' yet. Skipping compilation."
    exit 0
  fi
fi

# Step 3: Load book metadata
if [[ -f "$ROOT/book_metadata.txt" ]]; then
  TITLE="$(cat "$ROOT/book_metadata.txt" | head -n 1 | xargs)"
else
  TITLE="Manuscript"
fi
TITLE_SAFE="${TITLE// /_}"

echo -e "\n=== Step 3: Compiling Book Formats for: '$TITLE' ==="

# Verify python dependencies
if ! "$VENV_PYTHON" -c "import docx; import smartypants" 2>/dev/null; then
  echo "Installing python dependencies (python-docx, smartypants)..."
  if [[ "$VENV_PYTHON" == *".venv-docx"* ]]; then
    "$VENV_PYTHON" -m pip install python-docx smartypants || true
  else
    python3 -m pip install --user --break-system-packages python-docx smartypants || python3 -m pip install --user python-docx smartypants || true
  fi
fi

# Preprocess Markdown files for EPUB and PDF separately
TEMP_MD="$(mktemp)"
TEMP_MD_EPUB="${TEMP_MD}_epub"
TEMP_MD_PDF="${TEMP_MD}_pdf"
trap 'rm -f "$TEMP_MD" "$TEMP_MD_EPUB" "$TEMP_MD_PDF"' EXIT

# Generate DOCX and Assembled Markdown
"$VENV_PYTHON" "$MD_TO_DOCX" --assembled "$TEMP_MD"

# EPUB needs scene break representation
sed 's/__SCENE_BREAK__/---/g' "$TEMP_MD" > "$TEMP_MD_EPUB"

# PDF formatting prep
if [[ -f "$ROOT/Images/front_cover.jpg" ]]; then
  COVER_REPLACE="\\\\thispagestyle{empty}\\n\\\\null\\n\\\\begin{tikzpicture}[remember picture,overlay]\\n\\\\node at (current page.center) {\\\\includegraphics[width=\\\\paperwidth,height=\\\\paperheight]{Images/front_cover.jpg}};\\n\\\\end{tikzpicture}\\n\\\\let\\\\orgcleardoublepage\\\\cleardoublepage\\n\\\\let\\\\cleardoublepage\\\\clearpage\\n\\\\frontmatter\\n\\\\let\\\\cleardoublepage\\\\orgcleardoublepage\\n"
else
  COVER_REPLACE="\\\\frontmatter"
fi

perl -0777 -pe "s/# \{\\\\.unnumbered \\\\.unlisted\}\\\s*<div class=\"epub-title-page\">.*?<\/div>\\\s*\\\\pagebreak\\\s*\\\\frontmatter\\\s*/$COVER_REPLACE/gs" "$TEMP_MD" | \
perl -0777 -pe 's/<div class="chapter-opener-image"><img src="Images\/((chapter_\d+_open|epilogue_open)\.(jpg|jpeg|png))" alt=".*?" \/><\/div>\n\n\\pagebreak/\\chapteropenerimage{Images\/$1}/gs' | \
perl -0777 -pe 's/<[^>]+>//g' | \
sed -E -e 's/__SCENE_BREAK__/\\scenebreak/g' -e '/<div class="chapter-number">/d' > "$TEMP_MD_PDF"

# Compile Print PDFs via Pandoc and Tectonic
if command -v pandoc >/dev/null && (command -v tectonic >/dev/null || command -v Tectonic >/dev/null); then
  TECTONIC_CMD="tectonic"
  if ! command -v tectonic >/dev/null && command -v Tectonic >/dev/null; then
    TECTONIC_CMD="Tectonic"
  fi

  # Generate fonts.conf dynamically to ensure portability of fonts path
  cat <<EOF > "$WORD_DIR/fonts.conf"
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <dir>$WORD_DIR/fonts</dir>
  <dir>/usr/share/fonts/gsfonts</dir>
  <dir>/usr/share/fonts/liberation</dir>
  <cachedir>/tmp/fontconfig-${TITLE_SAFE}</cachedir>
</fontconfig>
EOF

  export FONTCONFIG_FILE="$WORD_DIR/fonts.conf"
  export FONTCONFIG_PATH="$WORD_DIR"

  echo "Compiling print PDF (6x9, no bleed)..."
  pandoc "$TEMP_MD_PDF" \
    --from markdown+smart \
    --template "$WORD_DIR/book.tex" \
    -H "$WORD_DIR/header.tex" \
    -V documentclass=book \
    -V classoption=twoside,openany \
    -V geometry:paperwidth=6in \
    -V geometry:paperheight=9in \
    -V geometry:twoside=true \
    -V geometry:inner=0.83in \
    -V geometry:outer=0.75in \
    -V geometry:top=0.6in \
    -V geometry:bottom=0.7in \
    -V geometry:headheight=14.5pt \
    -V geometry:headsep=18pt \
    -V geometry:footskip=24pt \
    -V geometry:includeheadfoot=true \
    -V fontsize=11pt \
    -V mainfont="EB Garamond" \
    --pdf-engine="$TECTONIC_CMD" \
    -o "$BUILD_DIR/${TITLE_SAFE}_Print.pdf"

  echo "Compiling print PDF (6x9, with bleed)..."
  pandoc "$TEMP_MD_PDF" \
    --from markdown+smart \
    --template "$WORD_DIR/book.tex" \
    -H "$WORD_DIR/header.tex" \
    -V documentclass=book \
    -V classoption=twoside,openany \
    -V geometry:paperwidth=6.125in \
    -V geometry:paperheight=9.25in \
    -V geometry:twoside=true \
    -V geometry:inner=0.83in \
    -V geometry:outer=0.75in \
    -V geometry:top=0.725in \
    -V geometry:bottom=0.825in \
    -V geometry:headheight=14.5pt \
    -V geometry:headsep=18pt \
    -V geometry:footskip=24pt \
    -V geometry:includeheadfoot=true \
    -V fontsize=11pt \
    -V mainfont="EB Garamond" \
    --pdf-engine="$TECTONIC_CMD" \
    -o "$BUILD_DIR/${TITLE_SAFE}_Print_Bleed.pdf"

  # Page Count Extraction
  if command -v pdfinfo >/dev/null; then
    PAGES=$(pdfinfo "$BUILD_DIR/${TITLE_SAFE}_Print.pdf" | grep Pages: | awk '{print $2}')
    printf "%s\n\n%s\n\n\x0c" "$TITLE" "$PAGES" > "$BUILD_DIR/${TITLE_SAFE}_Print.txt"
    echo "✓ Created: Releases/${TITLE_SAFE}_Print.txt (Page Count: $PAGES)"
  else
    echo "⚠ Warning: pdfinfo not found, could not extract page count"
    PAGES=400
  fi

  # paperback cover wrap PDFs
  if command -v convert >/dev/null || command -v magick >/dev/null; then
    CONVERT_CMD="convert"
    if ! command -v convert >/dev/null && command -v magick >/dev/null; then
      CONVERT_CMD="magick convert"
    fi
    COVER_PAGES="${PAGES}"
    echo "Compiling paperback cover wraps ($COVER_PAGES pages metadata)..."
    WHITE_W_PX=$("$VENV_PYTHON" -c "print(int(round((12.25 + $COVER_PAGES * 0.002252) * 300)))")
    CREAM_W_PX=$("$VENV_PYTHON" -c "print(int(round((12.25 + $COVER_PAGES * 0.0025) * 300)))")
    
    if [[ -f "$ROOT/Images/full_wrap.jpg" ]]; then
      $CONVERT_CMD "$ROOT/Images/full_wrap.jpg" -resize "${WHITE_W_PX}x2775!" -density 300 -units PixelsPerInch "$BUILD_DIR/${TITLE_SAFE}_Cover_White.pdf"
      $CONVERT_CMD "$ROOT/Images/full_wrap.jpg" -resize "${CREAM_W_PX}x2775!" -density 300 -units PixelsPerInch "$BUILD_DIR/${TITLE_SAFE}_Cover_Cream.pdf"
      cp "$BUILD_DIR/${TITLE_SAFE}_Cover_White.pdf" "$BUILD_DIR/${TITLE_SAFE}_Cover.pdf"
      echo "✓ Created Cover Wraps in Releases/"
    fi
  fi

  # DOCX exports with TOC page numbers extracted from the PDF
  echo "Compiling DOCX manuscripts with page-synced TOC..."
  "$VENV_PYTHON" "$MD_TO_DOCX" --pdf "$BUILD_DIR/${TITLE_SAFE}_Print.pdf"
  "$VENV_PYTHON" "$MD_TO_DOCX" --bleed --pdf "$BUILD_DIR/${TITLE_SAFE}_Print_Bleed.pdf"

  # Move outputs
  DOCX_OUT_NAME="$TITLE — master manuscript.docx"
  BLEED_OUT_NAME="$TITLE — master manuscript — bleed.docx"
  if [[ -f "$WORD_DIR/$DOCX_OUT_NAME" ]]; then
    mv "$WORD_DIR/$DOCX_OUT_NAME" "$BUILD_DIR/${TITLE_SAFE}_KDP.docx"
    echo "✓ Created: Releases/${TITLE_SAFE}_KDP.docx"
  fi
  if [[ -f "$WORD_DIR/$BLEED_OUT_NAME" ]]; then
    mv "$WORD_DIR/$BLEED_OUT_NAME" "$BUILD_DIR/${TITLE_SAFE}_KDP_Bleed.docx"
    echo "✓ Created: Releases/${TITLE_SAFE}_KDP_Bleed.docx"
  fi

else
  echo "⚠ PDF generation skipped: Install pandoc and tectonic to compile print PDFs."
  # Fall back to DOCX-only export when PDF tooling is unavailable
  "$VENV_PYTHON" "$MD_TO_DOCX"
  "$VENV_PYTHON" "$MD_TO_DOCX" --bleed
  DOCX_OUT_NAME="$TITLE — master manuscript.docx"
  BLEED_OUT_NAME="$TITLE — master manuscript — bleed.docx"
  if [[ -f "$WORD_DIR/$DOCX_OUT_NAME" ]]; then
    mv "$WORD_DIR/$DOCX_OUT_NAME" "$BUILD_DIR/${TITLE_SAFE}_KDP.docx"
    echo "✓ Created: Releases/${TITLE_SAFE}_KDP.docx"
  fi
  if [[ -f "$WORD_DIR/$BLEED_OUT_NAME" ]]; then
    mv "$WORD_DIR/$BLEED_OUT_NAME" "$BUILD_DIR/${TITLE_SAFE}_KDP_Bleed.docx"
    echo "✓ Created: Releases/${TITLE_SAFE}_KDP_Bleed.docx"
  fi
fi

# Compile EPUB
if command -v pandoc >/dev/null; then
  echo "Compiling EPUB ebook via Pandoc..."
  EPUB_ARGS=(
    "$TEMP_MD_EPUB"
    -o "$BUILD_DIR/${TITLE_SAFE}_Ebook.epub"
    --from markdown+smart
    --to epub3
    --toc
    --toc-depth=1
    -c "$EPUB_CSS"
    --epub-title-page=false
    --epub-embed-font="$WORD_DIR/fonts/EBGaramond-Regular.otf"
    --epub-embed-font="$WORD_DIR/fonts/EBGaramond-Italic.otf"
    --epub-embed-font="$WORD_DIR/fonts/EBGaramond-Bold.otf"
    --epub-embed-font="$WORD_DIR/fonts/EBGaramond-BoldItalic.otf"
    --metadata title="$TITLE"
    --metadata language="en"
  )
  
  if [[ -f "$ROOT/Images/front_cover.jpg" ]]; then
    EPUB_ARGS+=("--epub-cover-image=$ROOT/Images/front_cover.jpg")
  elif [[ -f "$WORD_DIR/cover.jpg" ]]; then
    EPUB_ARGS+=("--epub-cover-image=$WORD_DIR/cover.jpg")
  fi
  
  pandoc "${EPUB_ARGS[@]}"
  echo "✓ Created: Releases/${TITLE_SAFE}_Ebook.epub"
else
  echo "⚠ EPUB generation skipped: Install pandoc to compile EPUB."
fi

echo -e "\n=== Build Complete ==="
ls -lh "$BUILD_DIR"
