ATRAC Audio Video Converter - Windows MSI / macOS DMG ビルド

このZIPは完成済みのMSI/DMGではなく、GitHub Actionsで2つのインストーラーを作成するためのファイルです。

1. ZIPを解凍します。
2. 中身の3ファイルと .github/workflows/build-installers.yml をGitHubリポジトリのルートに配置してコミットします。
   ※ .github は隠しフォルダです。既存のアプリのソースを置き換える前にバックアップしてください。
3. GitHubの Actions タブで「Build ATRAC MSI and DMG」を選び「Run workflow」を実行します。
4. 完了したら、実行結果の Artifacts から ATRAC-Windows-MSI と ATRAC-macOS-DMG をダウンロードします。

注:
- 署名なしMSI/DMGのため、Windows SmartScreen / macOS Gatekeeperによる警告が出ることがあります。
- ffmpeg/ffprobeは同梱しますが、別ツール（atracdencなど）が必要な機能は別途用意が必要です。
- Windows/macOSでの完成品ビルド・起動・変換はまだ検証できていません。GitHub Actionsでエラーが出たらログを確認してください。
- GitHub Actionsの利用制限、ランナーや外部ソフトの変更でビルドに失敗する可能性があります。
