from pathlib import Path
import shutil

#상수는 대문자로 코딩: 정해진 값을 미리 셋팅 
DOWNLOADS = Path(r"C:\Users\student\Downloads")

# 확장자별 대상 폴더 (대소문자 구분없음)
EXT_TO_FOLDER = {
    ".jpg": "images",
    ".jpeg": "images",
    ".csv": "data",
    ".xlsx": "data",
    ".txt": "docs",
    ".doc": "docs",
    ".pdf": "docs",
    ".zip": "archive",
}

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def unique_path(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem = dest.stem
    suffix = dest.suffix
    parent = dest.parent
    i = 1
    while True:
        candidate = parent / f"{stem}_{i}{suffix}"
        if not candidate.exists():
            return candidate
        i += 1

def main():
    if not DOWNLOADS.exists():
        print(f"다운로드 폴더가 존재하지 않습니다: {DOWNLOADS}")
        return

    # 대상 폴더들 미리 생성
    target_dirs = {folder: DOWNLOADS / folder for folder in set(EXT_TO_FOLDER.values())}
    for d in target_dirs.values():
        ensure_dir(d)

    moved = 0
    for p in DOWNLOADS.iterdir():
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext in EXT_TO_FOLDER:
            target_folder = DOWNLOADS / EXT_TO_FOLDER[ext]
            dest = target_folder / p.name
            dest = unique_path(dest)
            try:
                shutil.move(str(p), str(dest))
                print(f"이동: {p.name} -> {dest}")
                moved += 1
            except Exception as e:
                print(f"오류: {p} -> {dest} : {e}")

    print(f"완료. 이동한 파일 수: {moved}")

if __name__ == "__main__":
    main()