# ATRAC Audio Video Converter

**Convert. Edit. Preserve. — 思い出の音楽を、もう一度。**

A desktop audio/video conversion and metadata editing project, originally developed to recover music from a Pioneer/carrozzeria car navigation system.

**Official download website:** https://atrac3-download.netlify.app/

[日本語](#日本語) · [English](#english) · [Bahasa Indonesia](#bahasa-indonesia)

---

## 日本語

### 概要
ATRAC Audio Video Converterは、音楽・動画の形式変換や音声タグ編集を行うデスクトップアプリです。カロッツェリアのナビから取り出したAT3音源を再生可能な形式に変換することが開発の出発点でした。

### 主な機能
- カロッツェリア由来のAT3（ATRAC3）ファイルの変換
- MP3・WAV・FLAC・M4Aなどの音声変換、対応する動画形式の変換
- Opus出力（対応するビルドの場合）
- 曲名・アーティスト・アルバムなどのタグ編集
- 複数ファイルの一括処理、フォルダー内ファイルの追加（対応するビルドの場合）
- ダーク／ライトテーマ

**注意：** AT3ファイルの仕様や保護状態によっては変換できない場合があります。すべての形式・機能の動作を保証するものではありません。

### ダウンロード
公式サイトから入手してください。

**https://atrac3-download.netlify.app/**

- Windows: 日本語版・英語版MSI
- macOS: PKG／DMG

インストーラーは実機での十分な動作検証が完了していません。重要なファイルは必ずバックアップしてください。Windowsの旧インストーラーからの更新では、以前のインストールの削除時に管理者権限が必要になる場合があります。

### 開発のきっかけ
かつて家族のデリカで聴いていた456曲を再び聴きたい、という思いから始まりました。初期のUIのないPythonスクリプトから、GUIを備えたコンバーターへと発展しました。

### 不具合報告
問題がある場合は [GitHub Issues](https://github.com/Himaya092-eng/ATRAC-Audio-Video-Converter-/issues) に、OS・アプリのバージョン・操作手順・エラー内容を書いてください。個人情報や著作権保護された音源は投稿しないでください。

---

## English

### Overview
ATRAC Audio Video Converter is a desktop project for converting audio/video files and editing audio metadata. It began as a way to access AT3 audio exported from a Pioneer/carrozzeria car navigation unit.

### Features
- Conversion of supported carrozzeria AT3 / ATRAC3 audio
- Audio conversion including MP3, WAV, FLAC, and M4A, plus supported video formats
- Opus output in builds that include it
- Metadata editing (title, artist, album, and more)
- Batch processing and folder import where supported
- Dark and light themes

Compatibility varies by source file and build. Some protected or proprietary AT3 files may not convert.

### Download
**https://atrac3-download.netlify.app/**

- Windows: Japanese and English MSI installers
- macOS: PKG and DMG installers

Installer behavior has not yet been comprehensively verified on real devices. Keep backups of important files.

### Report issues
Use [GitHub Issues](https://github.com/Himaya092-eng/ATRAC-Audio-Video-Converter-/issues). Include your OS, app version, steps to reproduce, and error message. Do not upload private data or copyrighted audio files.

---

## Bahasa Indonesia

### Tentang aplikasi
ATRAC Audio Video Converter adalah aplikasi desktop untuk konversi audio/video dan pengeditan metadata musik. Proyek ini dimulai untuk memulihkan file AT3 dari head unit Pioneer/carrozzeria.

### Fitur utama
- Konversi file AT3 / ATRAC3 carrozzeria yang didukung
- Konversi audio seperti MP3, WAV, FLAC, dan M4A
- Output Opus pada versi yang mendukung
- Edit judul, artis, album, dan metadata lainnya
- Pemrosesan beberapa file sekaligus dan impor folder pada versi yang mendukung
- Tema gelap dan terang

Tidak semua file atau format dijamin berhasil dikonversi.

### Unduh
**https://atrac3-download.netlify.app/**

- Windows: installer MSI bahasa Jepang dan Inggris
- macOS: installer PKG dan DMG

Instalasi belum diuji secara menyeluruh pada perangkat nyata. Simpan cadangan file penting.

---

## Development / 開発

Built with Python and related desktop libraries; conversion functions rely on external tools such as FFmpeg where available.

**Safety and rights:** Convert only files you are authorized to use. Back up original files before conversion. Do not assume lossy-to-lossy conversion restores audio quality.

**Project status:** Actively evolving. Features and compatibility can vary between released installers and the latest source code.
