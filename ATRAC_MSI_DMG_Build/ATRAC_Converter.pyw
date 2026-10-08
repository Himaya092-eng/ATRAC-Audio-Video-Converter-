import re, uuid, base64, io
import math
import os, shutil, sys, shutil, sys, struct, tempfile, subprocess, shutil, json, threading, ctypes, queue
import urllib.request
import urllib.parse
from html import unescape as html_unescape
import ssl
import plistlib
import platform
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageEnhance, ImageOps, ImageDraw, ImageFont
from tkinter import ttk, filedialog, messagebox, simpledialog
from pathlib import Path
from datetime import datetime
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_DND = True
except Exception:
    DND_FILES = None
    TkinterDnD = None
    HAS_DND = False


if sys.platform == "win32":
    try:
        ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
    except Exception:
        try: ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception: pass

APP_NAME="ATRAC Audio Video Converter v3.2.34 Windows + macOS + Web"

PIONEER_HEADER_SIZE=1928
FRAME_SIZE=384
SAMPLE_RATE=44100
CHANNELS=2
AVG_BYTES_PER_SEC=16537
BLOCK_ALIGN=384
ATRAC3_EXTRA=bytes.fromhex("0100001000000000000001000000")

DARK = {
    "bg":"#050b16","panel":"#0b1424","panel2":"#111f36","line":"#1b2c48",
    "text":"#f2f6fc","muted":"#7f93b0","accent":"#2b7fff","accent2":"#22c8ff",
    "hover":"#18304f","danger":"#ff5d6c","entry":"#08111f"
}
LIGHT = {
    "bg":"#edf2f9","panel":"#ffffff","panel2":"#f2f6fc","line":"#d8e1ee",
    "text":"#142036","muted":"#66778e","accent":"#1f6fff","accent2":"#2cb4ff",
    "hover":"#e2ebf8","danger":"#e34d5d","entry":"#f7f9fc"
}

ACTIVE_APP = None

HOME_ICON_DATA = {'youtube_music': 'iVBORw0KGgoAAAANSUhEUgAAADgAAAA4CAYAAACohjseAAAL10lEQVR42s1bW2xcRxn+5szZtY1iJ3aubYk34DohoXHStMQOBdHygPoCrUBEtCpCtEkT3oAnGjsglUo8IqCpmvCIUC9JIQhUKIlJJajUJq3bOkVt1YJ37YcCiS+x98yc3XNmPh7mrHft2PGetQM50khxrDNnvvnv3/9bkCQafax1y/dBAAQQT06CQ0Owr70KvvMO/A8/hP3oX8DMDHwdAoKIm5sh2tqAjRvBW28Fd+6E6OuF3LMHck0HvMr+cQx4nlsNPqIhgKQDJiUsgHh6CvalM+Dp08ArryBTKMweUsz9XGWDudsBbp9cDrzrs8B990F+6V5k1qx2bxjjQAqBBs6a8oljkqQlWcrnGfT3M8jlGAO0s8ujlRla6dN6Pq2Q7v9ql5DudzLjFjwagAZgBFDlOlnsf4x6ZIRm3rfTPPUDtHb2A+HEOIsD/VQdHbOHmj3oQmDqXULWAHb7qo4OBgP9LE2M01ZAWrvCAI27Q0MyeOEkVdcnqxLzs8sDdS2wfpZMgAaf7KI6daoqTWNWCGAitZIKWDx8iKXrDWwRoBZgGWDx8CGGKqhbZVEPOJ0f4cy+fU5qMuNs53oDm78Se40AFvf1MSz8sy6QWAqcGh5mkNvi7Mxv+t8Dm7eM3+Rsc0uOenh4SZC4puQuDlNv2lhVyf8zuNmVqGywaRPVxeGq86kLYGK8ulCg2pJz4BI3fkOtxNMGuU7qQn5Rx+NdFcBJRFrB7t+PpnwB8LMu0N5ojzGAn0VzYRRm/36ESoHJ+RcP9HFMQ7J4+NHE5rLL94Ay4/bxs9UYV/vzMj2x8bOMARYfPch4AVVFLThLsnj6Ny4U+Jlle7xKsDYA45p/1/7MFfDM9LMMAQanf3uV0xEJSoBEOH0FZvftaBkdhRDS5ZupMlvhckYTwQIwzS2wn7kD7N0LsW0HxLq1EEKAly6B770LXLgA8dp5+KWSy11lxn0zbXrseQANdGcO8q0hNLWtdmcRIlHRivT6j7hY14hqej5tIhm9/VPUx49Tj19mSLI0Ps7wzTdYPnuGpbNnGb41xHB8nCWSavwyg+NPU23fVs2OGpGmzLqMp3/AZTuJFEFjSGsZjo1RrV5N63mp7cLIDA3AsLWVwbEnWSIZFPIMjg4w7OlhlHF2UlkRwHImw6Cnh+qHR6lHR6lJBsd+Qd3aWs1tU9o7PUm9ejXDsTGXrxpDMIpoSar+/sakl4BTu3dRjeSpp6aoDjzCkufN2tmsVCpOJpF2ReKh9KgOHKCenmIw8k8Gu3uqWVPK+BgDDI485mJjFDknU5q+wuDjt9AIQSv81JIL7v4CdRRR/WWQasPGxHkkAXmpcim50BhgsGE9g8FBhuUSg3vuSQ/S82mFoLrlZpanp6teVD9/khHg6rcUmxmAQc8u6ihi8NwzDCtesZKIp1B14zsb0gCDZ5+ljmMWd+9yGpDGJpN8VZ183gE0JNUDDzjp1aueQtJ6kmFrK9VogcHL51xo8SStVy1eZ7OgeoF6Pq0nHchz5xiMFqhWtbp9693DzzopPvggLUmEkxNUmze7w9S7icy44HrsSeqZItXadbRCzIKzECyvWUO16aZEXUX9qub5tBDU69ZSF4sMnnoq0a5M/ZcPUG/uZHlqkggHz7IsBK1Io5qCautW5+YffmRu1pM4kPKO7QzHRqm+9z3qpmYH1PPrU7eKs3j4EYYkg+6ttBD1q6rwGAmP4dlBInjix+mMOZGeOnGCenSMJc+bq0IJwOjWW2lpaUiqt99k8WtfZbmSvSyVuSQuP5Q+9dgo9YnjyRmzqTy7fuIJerg4DJEmUzExTHMLxP6vw/7yOKS1gCevzj6EAKIInjFo6dmN5lMvIP7jiwj7+hCZCLQxIP2FmTIS9CR8E4PHj4Nf3w/b3AKYKB2zNvw2ULrjjvqzhyS/1J//HDVJ/ekdV3u5igS7u2mjcjU3TEqZchwzOHGC6hNbGNfmootkRuGOHSyT1F/4fP2lW+Lh9Z176Nn//LtaKtUhQQJAXy/E5Djk+x9AQCz9boW8NQYZKfGxgwfhvzGE8Gg/Sm1toIkcZyrmlW4QwAcfApMTwN5e9+16JEhCAPA++jc8TM/UD7DybNsO5EfhxREgZP3vSjlby2Xa29Hy+BPg6xegH3oIkUdXz1UAkBCehBeVYQp5iG3b0hHTADAzA88Pw6v452u9SADe2rUQExOJdBpgm6W7FC+K0Ny9FS2/+hXCc4MI168FRRUkhYAEIC5PQnR0LESKX0vdIMMQHpGuNBGzWiKWV5FbC2QyIIDy3/4K/yc/QfbKDASvVnmnml7yxRTnJeCZ5qb6X0pu1l4aB9a1JwdlemDWglKiNHEZ6vvfhXf3F9Hypz9DlqM54AQJC0Cs6wDGL805w5JSAGFamuGJ1rb6X0yugu+/C27OwfoZF9nqNHzErokSeR7Ur38Ne+deNP/0Z8gYumJ3vkOzBiabBXKdsO++n1LPALS1wsPGm+sHmHgnvPYa0NGBeNtWEFz6XeMugb5E+Pd3EH35K8g+9BBaRkbgyay7tvnElhAgCG7thmhfC1w4n9rbc9NN8NjVVT9AayEgIF5/A5yeBL72Vafci/XvrAWM6x+WtIJ+/HGgtw/Nf/g9MjIDej5g4sVDCwDcfz/s1BTk+dddSKqHRqk4qa4ueHbXbfWbLQlIH77WwHOnIA4eRCwlYM3VPocEsk2w0kP44oswvX1o+tGP0BQoCJkBjVn8sAKANYikBA4dAk+ehAw1KDOpwhl37gTU4JnUybaFoOrudjTDww87pmxesh3t+DSDkX8w+NY3XTVQySXrqViS2jD49repSaru7tTJdlkIhoNniVKD5VIEcObYz6mKMwzWr3P15OwBBEtr2hlsWO+S5HqriJqqPFi/nqpYZPDUsdTlkgGoP76Z0eQkYRsseOlJqlWrHLn08jnq2YK3AgTpaX/PJ4VkCLD48l8YFApUq1bRpCx4jRDU33jAFbwkqZ5/Lt0t1VIWu3qo44jFZ551IBuhLES1oRICVM88QxVFDHp6Gqcsnn8uAWjJci3plHKzGGDxnnuoozLV4BnqDRuSKiEd6WQABhs2MBg8S1UuM/ji3enpQ88nhaC+5RZGs6RTQhsGA0capg1jgMHtu6nyeeorVxgcOMDQk1VeZh5tSM93ZVJSAIdSUh14hGrqCoOREarduxNw2dS0oQFYPPIDR/5GUS3xO0q9Zk06gmc+N9rWxuDJJxmSVGMFqqMD1Dt3Msw2sVzTjygDDLNZ6p7bqI4epRorUJMsHvsFVWtbYy07IWk9j3r1auqxQg3xW9NVCo481nhXqRIeAKrt26mPP011+TJLJMsT49RvDlGf+TP12TPUbw2xNOF+F0yMM3j6aartn5qlNBqj7t0lF/sH5jRE5zRfStPTsLffjuZCwdV5y2i+EIBpakbceyewtxdi23aIde0Q8MBL/wHeex+4cAHe+fOQpZLLE5bbfMnl4L/1JrKtbfOaLzUNGP3b37B8HdpnC7XQ5oSS5Qw2+BmWABYXaJ8t2ACdPvQoo9rsZMUaoNkVb4BWKMbpw0s1QCvTTMZQq4DFvZ+58YYPFhtG6OtlpIIFp6CuMYQwQpW78YcQwlwnw0Jh0SGEa46RqIvDDG7adMOOkehNm6hTj5HMAxlcHGZxi5smNDcASFMBt2UL1fDwnG5uQ6NcNhnlCvb1MaqHdr+Oo1ysZE2f3ccwn7+m5FIP44VKsXj48P91GK8EcOY7hxgptULDeAuMU+oXTrLY1VWl3a/zOGUlluquLhZPnWK04uOUCwzEqolxBgMD1O0dcxudKzgQy8rERkcHg/5+licmqlJb8YHYBVTWkAzzear+x6g6O11icNVIc2bpcsnL1IShasajOztZPHKEYT6/rJHmZQ+lE0A8PY34pZeA07+DeOVvkIUC5AKj6LVD6fM/agDYXA686y43lH7vvfDb2pY9lN4YwEX+rAAA4qlJ2KEh8NVXId65CH74D8iP/gU7fQVSu6TatDSBbW3gTTcDXV3AbbcBfX2Qe/bAb2+vXkUcuz6GaLxN8F9ZyYwyPyYFzAAAAABJRU5ErkJggg==', 'youtube': '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', 'tiktok': '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', 'spotify': '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', 'apple_music': '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', 'car_at3': 'iVBORw0KGgoAAAANSUhEUgAAADgAAAA4CAYAAACohjseAAAFfUlEQVR42u2YWWyUVRTHf/d+U5jpPi0tlNKWrYOtBaTiUiRARNRGQbCaGNxwTfTJJSQY44vEBRUi8oAQDSIREY1KgqJWEJdgEaQC1bIoS62FLsMsbafTznz3+jDTlm7gI5J7niZz7j3n+93zv+d8M0JrrbmMTXKZmwE0gAbQABpAA2gADaABNIAG0AAaQANoAA3gJWiOCzm11qA1aEAAQiCEuAwAtUYrjbAk9APStkJIMeD7S9XEgL8Nte55+E5/K8G6Brpa20lISiQ1PwdnRtr/t4Jaa4QQhH1BfnrhLY5s2UHQewaNQiBJyRiJp+JmZr38NE53amy9JRFCxOSsFDouZyEEQva94lqpuOzjfkue59OgVe/5ChlTSj9VaTSCgX6tNLG7FK9cPHdvBbVGa4iGO/n0tic4truS/Kuuo/je+SSNyqTT38rhDZ9x6sAeSu9ZzO0fvt5XtpYc9A73EfJgstY6tk4Osl8phJRDx+/2K933MAaroLIV0mFRu3k7f+7eRW5xKQs+WoXbU9Cz2Hv0JPXV+wmcbqC9sYVA/T+kZI8kJW8UHS0+GqtrCZyqx5mWyojJHjKLxvdJ1nz4OC2/H0fbNmnjxjC67KpYJYWgraGJhqpDhJpacGW6yZ0xjeTc7Ni5WJJIW4gzvxwmWNdAQlIio6ZfSdq4MfFqCdrPtNB2pimmDkuSNWUSQoreCnaf9tZ5j3J059eUr3yJUJOXqlXv4M7PJ3wuQKuvEVeSmwVbVnJgzWZqv9nOne+tJXTWy8+vrqMr0EZyTjahRi9awITbZlO+4SVUJMIXDz5H3bdVpOaPJuwP0nauiWmPLGbu6mXsXvoGf3ywncyiCaQWjCbs9dP42x8UL57P7BXPcHD9x1S9up7EzAzSJ+Zjd3bRWF1L3pzp3LLuReq+28uXDy3D7oiilaJg7vVUfPk26HgFu0vdUnOchr2HSHJlMWH+HEKNXpprjxFt68RdWMDU0iJKHliIVoqTO3+kYEoZHc0+KpctJzNvPEuqPyVtbC6dgVa2zFnCb9u2MObdUjq8fg5+tZV5S19g9mvP8tf279m68GHOHTnB3hXvsn/tJrI9HpzpKbgy05GWJNIe5p+fDlCzcRu7nnqFlDGjcGakkTw6G23bnN1Xw4kdP9B86ChVy9cR8vuo+GQtOddOZlhKUnyc6W5AjZBQs3Eb/rY6rph1K+nj83AXFlAx8+0Buq58cjmt9lmuK3+MrKmTYh3XF+Tv3fsIFXlprK7Fd/w0qc4cHIkufn/zfdzD85ny+N0AnK7cQ7vtZeIdcxmW7CJKmIKbynCNSCfsD5Kck8XVT9/P2BvLULYiTCuTZpSTNdlDqMmLGJbAlMfvIntqEV2t7Zw6sIexpTPwVMzrNyMEDjRIh4XdFcF37BQjC4spWbIQYUnsSDSmYyF7moHd2UXgRD15nmuYOH8OuTeUsmjTGqrXbqbyyeUgwEpIIHfmNGY8/wRdoQ7U8Cgl9y3EPTGfSCiM98gJCq4oY3z5TEaUFBIJdVDz3udoW2E5hyMtSTgQJOtKD8X33s6iDWv4dfUmmg8eISEpEemwaD/nxelORytFemEeJQ8vAq1RURvpsHoaWu8dVBqtbISwENbQQ1wrhVYKKS2Qos/c7PD6ibSFcI1wk5DkAsDuiiAdVk+X1EqhbYV0OKBfmsDJeiKhMAmJThKzM2MxzosfOFlP2BfE4RxOYlYGriw3KhpFCDlolx180EPvq9nFLJ5c23YMQIg+B9Hd0YbeH8ujbBtpWReOP5j/PzxzX8DuTxeDG2Jd7xDvN/POq8IF9/cMazEwRv9hfv57cf/4F62g+blkAA2gATSABtAAGkADaAANoAE0gAbQABpAA2gADeDQ9i/muWxbJQ+Z5AAAAABJRU5ErkJggg=='}

def resource_path(name):
    base=getattr(sys,"_MEIPASS",None) or os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base,name)

TXT = {
    "ja": {
        "app":"ATRAC オーディオコンバーター・タグ編集ソフト",
        "audio_studio":"Audio Studio",
        "home":"⌂  ホーム","convert":"♫  変換","tags":"◇  タグ編集",
        "batch":"▣  一括タグ編集  Ctrl+K","youtube":"▶  YouTubeダウンロード","tiktok":"♪  TikTokダウンロード","player":"▶  メディアプレーヤー","music_match":"♪  音楽マッチDL","player_title":"メディアプレーヤー","player_hint":"音声・動画ファイルを追加して再生（Windows Media Player風）","player_add":"ファイル追加","player_clear":"リストクリア","player_play":"再生","player_pause":"一時停止","player_stop":"停止","player_prev":"前へ","player_next":"次へ","player_now":"再生中","music_match_title":"音楽マッチダウンロード","music_match_hint":"Apple Music / Amazon Music / LINE MUSIC / YouTube Music のリンク、または曲名を入力\n※各サービス本体からは取得せず、公開ソースからマッチ音声を保存します\n※NoteBurner型のDRM録音は行いません","youtube_title":"YouTubeダウンロード","tiktok_title":"TikTokダウンロード","youtube_hint":"YouTube のURLを1行に1つ入力（複数OK）","tiktok_hint":"TikTok URLを1行に1つ入力（複数OK）","remove_selected_url":"選択した項目を削除","clear_all_urls":"すべてクリア","calculator":"▦  電卓","cd":"💿  CD","format":"▣  フォーマット","format_title":"USB / SD フォーマット","format_drive":"ドライブ","format_fs":"ファイルシステム","format_label":"ボリューム名","format_refresh":"更新","format_start":"フォーマット開始","format_warning":"注意: フォーマットすると選択したドライブ内のデータはすべて消去されます。","format_confirm":"確認のため FORMAT と入力してください","format_blocked":"このドライブは安全のためフォーマットできません。","format_done":"フォーマット完了","cd_title":"CD 取り込み / 書き込み","cd_rip":"CDを取り込む","cd_burn":"CDに焼く","cd_drive":"CD/DVDドライブ","cd_folder":"保存先 / 音楽フォルダ","cd_browse":"参照","cd_refresh":"更新","cd_rip_note":"音楽CD → WAV / MP3 / FLAC","cd_burn_note":"音楽ファイル → オーディオCD（対応ドライブが必要）","calc_title":"電卓","calc_clear":"クリア","calc_back":"1文字削除","calc_error":"計算できません",
        "formats":"対応形式","light":"☀ ライトモード","dark":"☾ ダークモード",
        "hero":"オーディオコンバーター・タグ編集ソフト",
        "hero_sub":"FLAC・ADTS・MP3・M4A・WAV・動画ファイルをひとつのアプリで。",
        "open_convert":"変換を開く","tag_edit":"タグ編集","online_dl":"ダウンロード","youtube_dl":"YouTubeダウンロード","tiktok_dl":"TikTokダウンロード",
        "fast_convert":"高速変換","batch_edit":"一括タグ編集",
        "fast_sub":"音声・動画 → WAV / MP3 / M4A / FLAC / ADTS / MP4 / MKV / WEBM / MOV",
        "batch_sub":"Ctrl+K で複数ファイルをまとめて編集",
        "online_sub":"YouTube / TikTok を別々の画面から保存",
        "audio_convert":"オーディオ変換","+add":"+ ファイル追加",
        "remove":"選択した項目を削除","clear":"全部クリア",
        "output":"出力","bitrate":"ビットレート","start":"変換開始",
        "choose":"ファイルを選択","save":"保存  Ctrl+S",
        "title":"タイトル","artist":"アーティスト","album":"アルバム",
        "album_artist":"アルバムアーティスト","date":"年 / 日付",
        "genre":"ジャンル","track":"トラック","disc":"ディスク","comment":"コメント",
        "online_title":"オンラインダウンロード",
        "rights":"自分の動画、または保存する権利・許可があるコンテンツ用です。",
        "folder":"保存先","download":"ダウンロード開始",
        "batch_title":"一括タグ編集","auto_track":"トラック番号を自動連番","track_range":"開始番号 / 範囲","filename_title":"ファイル名をタイトルにする","title_common":"共通タイトル",
        "apply":"一括適用  Ctrl+S","language":"English",
        "need_files":"ファイルを追加してください。","ffmpeg":"FFmpeg が見つかりません。",
        "ffprobe":"ffprobe が見つかりません。","converted":"変換完了！",
        "tag_saved":"タグを保存しました。","need_url":"URLを入力してください。",
        "downloaded":"ダウンロード完了！","batch_done":"一括タグ編集が完了しました。","cover":"カバー画像","cover_choose":"画像を選択","cover_remove":"カバーを外す","cover_added":"カバー画像を設定しました。","cover_hint":"JPG / PNG を選択できます。","dl_ready":"待機中","dl_speed":"速度","dl_eta":"残り","dl_progress":"進捗","video_quality":"画質","audio_quality":"音質","batch_urls":"URLを1行に1つ入力（複数OK）","at3_encoder_missing":"AT3への変換には atracdenc が必要です。WindowsはGET_AT3_ENCODER.bat、MacはGET_AT3_ENCODER_MAC.commandを実行してください。","batch_download_done":"すべてのダウンロードが終わりました！","drop_files":"ここにファイルをドラッグ＆ドロップ","drop_files_sub":"またはボタンから選択","dnd_unavailable":"ドラッグ＆ドロップ機能を使うには tkinterdnd2 が必要です。"
    },
    "en": {
        "app":"ATRAC対応 オーディオ・ビデオコンバーター & Tag Editor",
        "audio_studio":"Audio Studio",
        "home":"⌂  Home","convert":"♫  Convert","tags":"◇  Tag Editor",
        "batch":"▣  Batch Edit  Ctrl+K","youtube":"▶  YouTube Download","tiktok":"♪  TikTok Download","player":"▶  Media Player","music_match":"♪  Music Match DL","player_title":"Media Player","player_hint":"Add audio/video files to play (Windows Media Player style)","player_add":"Add Files","player_clear":"Clear List","player_play":"Play","player_pause":"Pause","player_stop":"Stop","player_prev":"Previous","player_next":"Next","player_now":"Now Playing","music_match_title":"Music Match Download","music_match_hint":"Paste Apple Music / Amazon Music / LINE MUSIC / YouTube Music links, or song titles\n※Does not download from those services directly; matches public audio \n※No NoteBurner-style DRM recording","youtube_title":"YouTube Download","tiktok_title":"TikTok Download","youtube_hint":"Enter one YouTube URL per line (multiple OK)","tiktok_hint":"Enter one TikTok URL per line (multiple OK)","remove_selected_url":"Remove selected item","clear_all_urls":"Clear all","calculator":"▦  Calculator","cd":"💿  CD","format":"▣  Format","format_title":"USB / SD Format","format_drive":"Drive","format_fs":"File system","format_label":"Volume label","format_refresh":"Refresh","format_start":"Start format","format_warning":"Warning: formatting erases all data on the selected drive.","format_confirm":"Type FORMAT to confirm","format_blocked":"This drive is blocked for safety.","format_done":"Format complete","cd_title":"CD Rip / Burn","cd_rip":"Rip CD","cd_burn":"Burn CD","cd_drive":"CD/DVD drive","cd_folder":"Output / music folder","cd_browse":"Browse","cd_refresh":"Refresh","cd_rip_note":"Audio CD → WAV / MP3 / FLAC","cd_burn_note":"Audio files → Audio CD (compatible drive required)","calc_title":"Calculator","calc_clear":"Clear","calc_back":"Backspace","calc_error":"Cannot calculate",
        "formats":"Supported Formats","light":"☀ Light Mode","dark":"☾ Dark Mode",
        "hero":"Audio Converter & Tag Editor",
        "hero_sub":"FLAC, ADTS, MP3, M4A, WAV and video files in one app.",
        "open_convert":"Open Converter","tag_edit":"Tag Editor","online_dl":"Downloads","youtube_dl":"YouTube Download","tiktok_dl":"TikTok Download",
        "fast_convert":"Fast Conversion","batch_edit":"Batch Tag Editing",
        "fast_sub":"音声・動画 → WAV / MP3 / M4A / FLAC / ADTS / MP4 / MKV / WEBM / MOV",
        "batch_sub":"Edit multiple files together with Ctrl+K",
        "online_sub":"Save from YouTube / TikTok",
        "audio_convert":"Audio Converter","+add":"+ Add Files",
        "remove":"Remove Selected","clear":"Clear All",
        "output":"Output","bitrate":"Bitrate","start":"Start Conversion",
        "choose":"Choose File","save":"Save  Ctrl+S",
        "title":"Title","artist":"Artist","album":"Album",
        "album_artist":"Album Artist","date":"Year / Date",
        "genre":"Genre","track":"Track","disc":"Disc","comment":"Comment",
        "online_title":"Online Download",
        "rights":"Use only for videos you own or content you have permission or rights to save.",
        "folder":"Output Folder","download":"Start Download",
        "batch_title":"Batch Tag Editor","auto_track":"Auto-number tracks","track_range":"Start / Range","filename_title":"Use filename as title","title_common":"Common Title",
        "apply":"Apply to All  Ctrl+S","language":"日本語",
        "need_files":"Add files first.","ffmpeg":"FFmpeg was not found.",
        "ffprobe":"ffprobe was not found.","converted":"Conversion complete!",
        "tag_saved":"Tags saved.","need_url":"Enter a URL.",
        "downloaded":"Download complete!","batch_done":"Batch editing complete.","cover":"Cover Art","cover_choose":"Choose Image","cover_remove":"Remove Cover","cover_added":"Cover art set.","cover_hint":"Choose a JPG or PNG image.","dl_ready":"Ready","dl_speed":"Speed","dl_eta":"ETA","dl_progress":"Progress","video_quality":"Video Quality","audio_quality":"Audio Quality","batch_urls":"One URL per line (multiple URLs supported)","at3_encoder_missing":"AT3 output requires atracdenc. On Windows run GET_AT3_ENCODER.bat; on macOS run GET_AT3_ENCODER_MAC.command.","batch_download_done":"All downloads finished!","drop_files":"Drag & drop files here","drop_files_sub":"or choose them with the button","dnd_unavailable":"Drag and drop requires tkinterdnd2."
    }
}

def app_dir():
    return os.path.dirname(os.path.abspath(sys.argv[0]))



def _sanitize_output_folder_name(name):
    """Make a Windows-safe folder name for duplicate-output separation."""
    name=str(name or "folder").strip() or "folder"
    name=re.sub(r'[<>:\"/\\|?*]+', '_', name)
    name=name.rstrip(' .') or "folder"
    return name[:80]

def _compression_output_map(files, outdir, name_func):
    """
    Build safe compression destinations while keeping source folders together.

    Important: when files come from more than one source folder, ALL outputs are
    placed under a subfolder named after their original parent folder.  This
    prevents a unique file such as TRACK20 from being left loose in the output
    root while TRACK01..TRACK19 are grouped because their names are duplicated.
    """
    outdir=Path(outdir)
    files=list(files)
    desired=[str(name_func(src)) for src in files]

    parent_paths=[]
    for src in files:
        try:
            parent_paths.append(os.path.normcase(os.path.abspath(str(Path(src).parent))))
        except Exception:
            parent_paths.append(str(Path(src).parent).lower())
    multiple_source_folders=len(set(parent_paths))>1

    counts={}
    for n in desired:
        k=n.lower()
        counts[k]=counts.get(k,0)+1

    used=set()
    folder_aliases={}
    used_folder_names={}
    result={}

    def source_folder_for(src):
        parent_path=os.path.normcase(os.path.abspath(str(Path(src).parent)))
        if parent_path in folder_aliases:
            return folder_aliases[parent_path]
        base=_sanitize_output_folder_name(Path(src).parent.name or "folder")
        name=base
        idx=2
        while name.lower() in used_folder_names:
            name=f"{base}_{idx}"
            idx+=1
        used_folder_names.add(name.lower())
        folder_aliases[parent_path]=name
        return name

    for src,name in zip(files,desired):
        key=name.lower()

        # Preserve folder grouping whenever more than one source folder is in
        # the batch.  For a single-source-folder batch, keep the old flat layout
        # unless a duplicate filename needs separation.
        if multiple_source_folders:
            target_dir=outdir/source_folder_for(src)
            candidate=target_dir/name
        elif counts.get(key,0)>1:
            target_dir=outdir/source_folder_for(src)
            candidate=target_dir/name
        else:
            target_dir=outdir
            candidate=target_dir/name

        # Last-resort collision protection without moving just one track out of
        # its album/source folder.
        if str(candidate).lower() in used:
            stem=Path(name).stem
            suffix=Path(name).suffix
            idx=2
            while True:
                alt=target_dir/f"{stem}_{idx}{suffix}"
                if str(alt).lower() not in used:
                    candidate=alt
                    break
                idx+=1

        # Never overwrite/read the exact same source file in-place.
        try:
            same_as_source = candidate.resolve() == Path(src).resolve()
        except Exception:
            same_as_source = os.path.abspath(str(candidate)) == os.path.abspath(str(src))
        if same_as_source:
            target_dir=outdir/"圧縮後"
            candidate=target_dir/name

        target_dir.mkdir(parents=True,exist_ok=True)
        used.add(str(candidate).lower())
        result[src]=str(candidate)
    return result

def tool(name):
    exe=name+".exe" if os.name=="nt" and not name.lower().endswith(".exe") else name

    # PyInstaller one-file extracts bundled binaries into sys._MEIPASS.
    base=getattr(sys,"_MEIPASS",None)
    if base:
        p=os.path.join(base,exe)
        if os.path.exists(p):
            return p

    # Also check beside the executable/source for development builds.
    try:
        appdir=os.path.dirname(sys.executable if getattr(sys,"frozen",False) else os.path.abspath(__file__))
        p=os.path.join(appdir,exe)
        if os.path.exists(p):
            return p
    except:
        pass

    aliases=[exe,name]
    if sys.platform=="darwin" and name in ("cdparanoia","cd-paranoia"):
        aliases += ["cd-paranoia","cdparanoia"]
    for candidate in aliases:
        found=shutil.which(candidate)
        if found:
            return found
    # Finder-launched macOS apps inherit a minimal PATH. Search common package-manager paths.
    if sys.platform=="darwin":
        for base in ("/opt/homebrew/bin","/usr/local/bin","/opt/local/bin"):
            for candidate in aliases:
                q=os.path.join(base,candidate)
                if os.path.isfile(q) and os.access(q,os.X_OK):
                    return q
    return None


def run(cmd):
    flags=getattr(subprocess,"CREATE_NO_WINDOW",0)
    p=subprocess.run(cmd,capture_output=True,text=True,creationflags=flags)
    if p.returncode:
        raise RuntimeError((p.stderr or p.stdout or "Process failed").strip())
    return p.stdout

def build_atrac3_riff(src,dst):
    data=open(src,"rb").read()
    if len(data)<=PIONEER_HEADER_SIZE or data[:3]!=b"VA3":
        raise ValueError("Unsupported or damaged Pioneer AT3 file.")
    payload=data[PIONEER_HEADER_SIZE:]
    if len(payload)%FRAME_SIZE:
        raise ValueError("ATRAC3 payload alignment error.")
    fmt=struct.pack("<HHIIHHH",0x0270,CHANNELS,SAMPLE_RATE,AVG_BYTES_PER_SEC,BLOCK_ALIGN,0,len(ATRAC3_EXTRA))+ATRAC3_EXTRA
    chunks=b"fmt "+struct.pack("<I",len(fmt))+fmt+b"data"+struct.pack("<I",len(payload))+payload
    open(dst,"wb").write(b"RIFF"+struct.pack("<I",4+len(chunks))+b"WAVE"+chunks)

def _media_duration_seconds(path):
    ffprobe=tool("ffprobe")
    if not ffprobe:
        return None
    try:
        out=run([ffprobe,"-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",path]).strip()
        val=float(out)
        return val if val>0 else None
    except Exception:
        return None

def _ffmpeg_run_progress(cmd,duration,progress_cb=None):
    # FFmpeg's -progress output gives real in-file progress instead of only
    # updating after each file has finished. The output path is always last.
    pcmd=cmd[:-1]+["-progress","pipe:1","-nostats",cmd[-1]]
    flags=getattr(subprocess,"CREATE_NO_WINDOW",0)
    p=subprocess.Popen(pcmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,
                       bufsize=1,universal_newlines=True,creationflags=flags)
    app=globals().get("ACTIVE_APP")
    try:
        if app is not None:
            try: app._track_proc(p)
            except Exception: pass
        if progress_cb:
            progress_cb(0.0)
        if p.stdout:
            for raw in p.stdout:
                if app is not None and getattr(app,"_cancel_work",None) is not None and app._is_work_cancelled():
                    try:
                        app._kill_process(p,timeout=1.0)
                    except Exception:
                        try: p.kill()
                        except Exception: pass
                    raise RuntimeError("処理をキャンセルしました。")
                line=raw.strip()
                if line.startswith("out_time=") and duration:
                    try:
                        t=line.split("=",1)[1]
                        hh,mm,ss=t.split(":")
                        elapsed=float(hh)*3600+float(mm)*60+float(ss)
                        progress_cb(max(0.0,min(0.995,elapsed/duration)))
                    except Exception:
                        pass
                elif line=="progress=end" and progress_cb:
                    progress_cb(1.0)
        stderr=p.stderr.read() if p.stderr else ""
        rc=p.wait()
        if app is not None and app._is_work_cancelled():
            raise RuntimeError("処理をキャンセルしました。")
        if rc:
            raise RuntimeError((stderr or "FFmpeg conversion failed").strip())
        if progress_cb:
            progress_cb(1.0)
    finally:
        try:
            if app is not None:
                try: app._untrack_proc(p)
                except Exception: pass
            if p.stdout: p.stdout.close()
            if p.stderr: p.stderr.close()
        except Exception:
            pass

def convert_audio(ffmpeg,src,dst,outfmt,bitrate,atracdenc=None,progress_cb=None,sample_rate=None):
    ext=os.path.splitext(src)[1].lower()
    with tempfile.TemporaryDirectory() as td:
        actual=src
        if ext==".at3":
            # Pioneer VA3 recordings are decoded by wrapping their ATRAC3 payload.
            actual=os.path.join(td,"wrapped.wav")
            build_atrac3_riff(src,actual)

        if outfmt=="AT3 (ATRAC3)":
            if not atracdenc:
                raise RuntimeError("atracdenc is required for AT3 output.")
            pcm=os.path.join(td,"atrac_input.wav")
            run([ffmpeg,"-y","-hide_banner","-loglevel","error","-i",actual,
                 "-vn","-ar","44100","-ac","2","-c:a","pcm_s16le",pcm])
            run([atracdenc,"-e","atrac3","--container","riff","-i",pcm,"-o",dst])
            if progress_cb: progress_cb(1.0)
            return

        cmd=[ffmpeg,"-y","-hide_banner","-loglevel","error","-i",actual]
        sr_args=[]
        if sample_rate:
            try:
                sr=int(str(sample_rate).replace("Hz","").replace(" ",""))
                if sr > 0:
                    sr_args=["-ar",str(sr)]
            except Exception:
                sr_args=[]
        # libopus requires 48000, 24000, 16000, 12000, or 8000 Hz.
        # Always resample audio to 48 kHz for Opus, irrespective of GUI settings.
        if outfmt=="OPUS":
            sr_args=["-ar","48000"]
        if outfmt=="WAV":
            cmd+=["-vn","-c:a","pcm_s16le"]+sr_args+[dst]
        elif outfmt=="MP3":
            cmd+=["-vn","-c:a","libmp3lame","-b:a",bitrate]+sr_args+[dst]
        elif outfmt=="OPUS":
            cmd+=["-vn","-c:a","libopus","-b:a",bitrate,"-vbr","on"]+sr_args+[dst]
        elif outfmt=="M4A":
            cmd+=["-vn","-c:a","aac","-b:a",bitrate]+sr_args+["-movflags","+faststart",dst]
        elif outfmt=="FLAC":
            cmd+=["-vn","-c:a","flac"]+sr_args+[dst]
        elif outfmt=="ADTS (.adts)":
            cmd+=["-vn","-c:a","aac","-b:a",bitrate]+sr_args+["-f","adts",dst]
        elif outfmt=="MP4 (H.264/AAC)":
            cmd+=["-map","0:v:0?","-map","0:a:0?","-c:v","libx264","-preset","medium",
                  "-crf","20","-c:a","aac","-b:a",bitrate]+sr_args+["-movflags","+faststart",dst]
        elif outfmt=="MKV (H.264/AAC)":
            cmd+=["-map","0:v:0?","-map","0:a:0?","-c:v","libx264","-preset","medium",
                  "-crf","20","-c:a","aac","-b:a",bitrate]+sr_args+[dst]
        elif outfmt=="WEBM (VP9/Opus)":
            cmd+=["-map","0:v:0?","-map","0:a:0?","-c:v","libvpx-vp9","-crf","30","-b:v","0",
                  "-c:a","libopus","-b:a",bitrate]+sr_args+[dst]
        elif outfmt=="MOV (H.264/AAC)":
            cmd+=["-map","0:v:0?","-map","0:a:0?","-c:v","libx264","-preset","medium",
                  "-crf","20","-c:a","aac","-b:a",bitrate,"-movflags","+faststart",dst]
        else:
            raise ValueError("Unknown output format")
        _ffmpeg_run_progress(cmd,_media_duration_seconds(actual),progress_cb)

def read_tags(ffprobe,path):
    out=run([ffprobe,"-v","error","-show_entries","format_tags","-of","json",path])
    raw=json.loads(out or "{}").get("format",{}).get("tags",{}) or {}
    return {str(k).lower():str(v) for k,v in raw.items()}

def write_tags(ffmpeg,path,tags):
    folder=os.path.dirname(path)
    stem,ext=os.path.splitext(os.path.basename(path))
    tmp=os.path.join(folder,stem+".__tagtmp__"+ext)
    cmd=[ffmpeg,"-y","-hide_banner","-loglevel","error","-i",path,"-map","0","-c","copy"]
    for k,v in tags.items(): cmd+=["-metadata",f"{k}={v}"]
    cmd.append(tmp)
    try:
        run(cmd); os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):
            try: os.remove(tmp)
            except: pass


def _prepare_cover_bytes(cover_path):
    import io
    from PIL import Image
    with Image.open(cover_path) as im:
        # Car stereos tend to be happiest with JPEG cover art.
        if im.mode not in ("RGB","L"):
            im=im.convert("RGB")
        elif im.mode=="L":
            im=im.convert("RGB")
        im.thumbnail((1200,1200))
        buf=io.BytesIO()
        im.save(buf,format="JPEG",quality=90)
        return buf.getvalue(),"image/jpeg"


def _replace_cover_art(path,cover_path):
    ext=os.path.splitext(path)[1].lower()
    data,mime=_prepare_cover_bytes(cover_path)

    if ext==".mp3":
        from mutagen.id3 import ID3, ID3NoHeaderError, APIC
        try:
            tags=ID3(path)
        except ID3NoHeaderError:
            tags=ID3()
        tags.delall("APIC")
        tags.add(APIC(encoding=3,mime=mime,type=3,desc="Cover",data=data))
        tags.save(path,v2_version=3)
        return

    if ext in (".m4a",".mp4"):
        from mutagen.mp4 import MP4, MP4Cover
        audio=MP4(path)
        if audio.tags is None:
            audio.add_tags()
        audio.tags["covr"]=[MP4Cover(data,imageformat=MP4Cover.FORMAT_JPEG)]
        audio.save()
        return

    if ext==".flac":
        from mutagen.flac import FLAC, Picture
        audio=FLAC(path)
        audio.clear_pictures()
        pic=Picture()
        pic.type=3
        pic.mime=mime
        pic.desc="Cover"
        pic.data=data
        audio.add_picture(pic)
        audio.save()
        return

    raise ValueError("カバー画像変更は MP3 / M4A / MP4 / FLAC に対応しています。")


def write_tags_with_cover(ffmpeg,path,tags,cover_path=None,remove_cover=False):
    write_tags(ffmpeg,path,tags)
    if cover_path:
        _replace_cover_art(path,cover_path)


def _read_utf16z_field(buf, offset, size):
    """Read one fixed-width UTF-16LE, NUL-terminated text field."""
    if offset < 0 or offset >= len(buf):
        return ""
    raw = buf[offset:min(len(buf), offset + size)]
    try:
        text = raw.decode("utf-16le", errors="ignore").split("\x00", 1)[0]
    except Exception:
        return ""
    return text.strip().strip("\ufeff")


def _find_navirecdata_root(path):
    """Return the NAVIRECDATA directory containing path, if present."""
    try:
        cur = Path(path).resolve()
    except Exception:
        cur = Path(path)
    if cur.is_file():
        cur = cur.parent
    for candidate in [cur] + list(cur.parents):
        if candidate.name.upper() == "NAVIRECDATA":
            return str(candidate)
    return ""


def _carrozzeria_opl_number(path):
    """Extract OPLxxx number from an AT3 path."""
    try:
        parts = Path(path).parts
    except Exception:
        return None
    for part in reversed(parts):
        m = re.fullmatch(r"OPL(\d{3})", str(part), flags=re.I)
        if m:
            return int(m.group(1))
    return None


def _carrozzeria_track_number(path):
    m = re.search(r"TRACK\s*0*(\d+)", Path(path).stem, flags=re.I)
    return int(m.group(1)) if m else None


def _find_dat_recursive(root, filename):
    if not root or not os.path.isdir(root):
        return ""
    target = filename.lower()
    try:
        for d, _, files in os.walk(root):
            for name in files:
                if name.lower() == target:
                    return os.path.join(d, name)
    except Exception:
        pass
    return ""



class App:
    def __init__(self,root):
        self.root=root
        self.root.title(APP_NAME)
        self.root.geometry("1180x760")
        self.root.minsize(1020,680)
        try:
            dpi=root.winfo_fpixels("1i")
            root.tk.call("tk","scaling",dpi/72.0)
        except: pass

        global ACTIVE_APP
        ACTIVE_APP=self
        self.theme="light"
        try:
            ctk.set_appearance_mode("Light")
        except Exception:
            pass
        self.lang="ja"
        self._home_icon_cache={}
        self.files=[]
        self.car_at3_files=[]
        self.car_at3_outfmt=tk.StringVar(value="MP3")
        self.car_at3_bitrate=tk.StringVar(value="160k")
        self.car_at3_sample_rate=tk.StringVar(value="44100")
        self.car_at3_restore_tags=tk.BooleanVar(value=True)
        self.car_at3_delete_source=tk.BooleanVar(value=False)
        self.car_at3_navirecdata=tk.StringVar(value="")
        self.car_at3_busy=False
        self.outfmt=tk.StringVar(value="MP3")
        self.bitrate=tk.StringVar(value="192k")
        self.sample_rate=tk.StringVar(value="元のまま")
        self.video_compress_files=[]
        self.video_compress_quality=tk.StringVar(value="標準")
        self.video_compress_resolution=tk.StringVar(value="元のまま")
        self.video_compress_audio_bitrate=tk.StringVar(value="128k")
        self.video_compress_speed=tk.StringVar(value="高速")
        self.video_compress_outdir=tk.StringVar(value=os.path.join(os.path.expanduser("~"),"Videos","Compressed"))
        self.video_compress_delete_source=tk.BooleanVar(value=False)
        self.video_compress_busy=False
        self.audio_compress_files=[]
        self.audio_compress_format=tk.StringVar(value="MP3")
        self.audio_compress_bitrate=tk.StringVar(value="192k")
        self.audio_compress_outdir=tk.StringVar(value=os.path.join(os.path.expanduser("~"),"Music","Compressed"))
        self.audio_compress_delete_source=tk.BooleanVar(value=False)
        self.audio_compress_busy=False
        self.image_compress_files=[]
        self.image_compress_format=tk.StringVar(value="元の形式")
        self.image_compress_quality=tk.StringVar(value="標準")
        self.image_compress_max_size=tk.StringVar(value="元のまま")
        self.image_compress_outdir=tk.StringVar(value=os.path.join(os.path.expanduser("~"),"Pictures","Compressed"))
        self.image_compress_delete_source=tk.BooleanVar(value=False)
        self.image_compress_busy=False
        # Safety: source files are never deleted unless the user explicitly enables this.
        self.delete_source_after_convert=tk.BooleanVar(value=False)
        self.online_fmt=tk.StringVar(value="MP4")
        self.video_quality=tk.StringVar(value="1080p")
        self.audio_quality=tk.StringVar(value="320 kbps")
        self.online_sample_rate=tk.StringVar(value="元のまま")
        self.online_url=tk.StringVar()
        # Persistent download status variables. These must exist before any
        # download/service page is built or the background UI bridge starts.
        self.dl_percent=tk.StringVar(value="0%")
        self.dl_speed=tk.StringVar(value="-")
        self.dl_eta=tk.StringVar(value="-")
        self.dl_batch_index=1
        self.dl_batch_total=1
        self.online_folder=tk.StringVar()
        # Thread-safe download UI bridge. Worker threads never touch Tk directly.
        self._dl_ui_queue=queue.Queue()
        # Download state lives outside individual pages, so switching pages does not
        # cancel a download or lose its progress display.
        # Reuse the persistent download status variables across page changes.
        self._dl_progress_value=0.0
        self.download_active=False
        # Global cancel / process tracking so closing the app stops everything.
        self._app_closing=False
        self._cancel_work=threading.Event()
        self._user_cancelled=False
        self.cancelbtn=None
        self._dl_started_at=0.0
        self._tracked_procs=[]
        self._tracked_procs_lock=threading.Lock()
        # Separate streaming-service pages. These pages do not bypass DRM or extract
        # protected streams; they keep links/metadata separate and open the official service.
        self.service_urls={"spotify":"","apple_music":"","youtube_music":"","youtube":"","tiktok":"","music_match":""}
        self._svc_settings={}
        self.service_text_widget=None
        self.service_active=None
        self.tag_path=tk.StringVar()
        self.cover_path=tk.StringVar()
        self.tagvars={k:tk.StringVar() for k in ["title","artist","album","album_artist","date","genre","track","disc","comment"]}

        # Keep batch-tag editor state when switching pages, language or Light/Dark mode.
        self.batch_files=[]
        self.batch_auto=tk.BooleanVar(value=False)
        self.batch_track_range=tk.StringVar(value="1")
        self.batch_use_filename=tk.BooleanVar(value=False)
        self.batch_tagvars={k:tk.StringVar() for k in ["title","artist","album","album_artist","date","genre","disc","comment"]}
        self.batch_rename_prefix=tk.StringVar()
        self.batch_rename_start=tk.StringVar(value="1")
        self.batch_rename_digits=tk.StringVar(value="2")
        self.batch_cover=tk.StringVar()

        # Standalone file/folder modified-time editor state.
        self.mtime_items=[]
        self.mtime_value=tk.StringVar(value="")

        # Local Library (TuneFab-style local history / local media view)
        self.library_items=[]
        self.library_search=tk.StringVar(value="")
        self.library_filter=tk.StringVar(value="すべて")
        self.library_sort=tk.StringVar(value="追加日時")
        self.library_status=tk.StringVar(value="")
        self.library_current_path=""
        self._library_meta_cache={}
        self._library_refresh_token=0
        self._library_refresh_after=None
        self._ensure_library_dirs()
        self.online_folder.set(self._library_download_dir())

        self.player_files=[]
        self.player_vol=tk.DoubleVar(value=80)
        self._vol_after=None
        self.player_index=0
        self.player_proc=None
        self.player_paused=False
        self.player_now=tk.StringVar(value="")
        self.player_continuous=tk.BooleanVar(value=True)
        self.player_stop_requested=False
        self.player_gen=0
        self.player_duration=0.0
        self.player_seek_offset=0.0
        self.player_started_at=0.0
        self.player_seeking=False
        self.player_pos=tk.DoubleVar(value=0.0)
        self.player_time_label=tk.StringVar(value="0:00 / 0:00")

        # Batch folder-rename state (renames folders only; files inside are untouched)
        self.rename_folders=[]
        self.rename_prefix=tk.StringVar(value="")
        self.rename_start=tk.StringVar(value="1")
        self.rename_digits=tk.StringVar(value="2")
        # Batch rename of files inside folders (folders themselves stay named as-is)
        self.inner_files=[]
        self.inner_include_subfolders=tk.BooleanVar(value=False)
        self.inner_prefix=tk.StringVar(value="")
        self.inner_start=tk.StringVar(value="1")
        self.inner_digits=tk.StringVar(value="2")

        self._build_shell()
        self.show_page("home")
        self.root.bind("<Control-k>",self.open_batch_tags)
        self.root.bind("<Control-o>",lambda e:self.add_files())
        self.root.after(80,self._poll_dl_ui_queue)
        # Ensure ffplay / preview processes are killed when the app window closes.
        try:
            self.root.protocol("WM_DELETE_WINDOW", self._on_app_close)
        except Exception:
            pass

    def _post_dl_ui(self,kind,*args):
        try:
            self._dl_ui_queue.put_nowait((kind,args))
        except Exception:
            pass

    def _poll_dl_ui_queue(self):
        """Drain download events on the Tk main thread so Windows stays responsive."""
        try:
            # Collapse bursts of progress events so the Tk event loop is not flooded.
            latest_progress=None
            processed=0
            while processed < 200:
                try:
                    kind,args=self._dl_ui_queue.get_nowait()
                except queue.Empty:
                    break
                processed += 1
                if kind=="progress":
                    latest_progress=args
                    continue
                if latest_progress is not None:
                    try:self._update_dl_ui(*latest_progress)
                    except Exception:pass
                    latest_progress=None
                try:
                    if kind=="reset":
                        self._reset_dl_ui()
                    elif kind=="status":
                        self.dl_percent.set(str(args[0]) if args else "")
                    elif kind=="success":
                        self._download_success()
                    elif kind=="error":
                        self._download_error(str(args[0]) if args else "Download error")
                    elif kind=="askyesno":
                        title, msg, response_q = args
                        try: response_q.put(bool(messagebox.askyesno(title, msg)))
                        except Exception: response_q.put(False)
                    elif kind=="askstring":
                        title, msg, response_q = args
                        try: response_q.put(simpledialog.askstring(title, msg, parent=self.root))
                        except Exception: response_q.put(None)
                except Exception:
                    pass
            if latest_progress is not None:
                try:self._update_dl_ui(*latest_progress)
                except Exception:pass
        finally:
            try:
                self.root.after(80,self._poll_dl_ui_queue)
            except Exception:
                pass

    def _ask_ui_yesno(self,title,msg):
        """Show a yes/no dialog on the Tk thread even when called by a worker."""
        if threading.current_thread() is threading.main_thread():
            return bool(messagebox.askyesno(title,msg))
        q=queue.Queue(maxsize=1)
        self._post_dl_ui("askyesno",title,msg,q)
        try:return bool(q.get(timeout=300))
        except Exception:return False

    def _ask_ui_string(self,title,msg):
        """Show a text prompt on the Tk thread even when called by a worker."""
        if threading.current_thread() is threading.main_thread():
            try:return simpledialog.askstring(title,msg,parent=self.root)
            except Exception:return None
        q=queue.Queue(maxsize=1)
        self._post_dl_ui("askstring",title,msg,q)
        try:return q.get(timeout=300)
        except Exception:return None

    def p(self): return LIGHT
    def tr(self,k): return TXT[self.lang].get(k,k)

    def _get_home_icon(self,key,size=(50,50)):
        cache_key=(key,size)
        if cache_key in getattr(self,"_home_icon_cache",{}):
            return self._home_icon_cache[cache_key]
        data=HOME_ICON_DATA.get(key)
        if not data:
            return None
        try:
            raw=base64.b64decode(data)
            im=Image.open(io.BytesIO(raw)).convert("RGBA")
            icon=ctk.CTkImage(light_image=im,dark_image=im,size=size)
            self._home_icon_cache[cache_key]=icon
            return icon
        except Exception:
            return None

    def clear_content(self):
        for w in self.content.winfo_children():
            try: w.destroy()
            except Exception: pass
        # These are page-local widgets.  Do not keep stale references after a
        # page switch; the download itself continues in its worker thread.
        self.onprog=None
        self.downbtn=None
        self.cancelbtn=None
        self.online_folder_label=None

    def style_button(self,b,primary=False):
        p=self.p()
        accent=p.get("accent","#2563eb")
        accent2=p.get("accent2",accent)
        panel2=p.get("panel2",p.get("panel","#2b2b2b"))
        text=p.get("text","#ffffff")
        # Some older palettes do not define "hover", so fall back safely.
        hover=p.get("hover",accent2 if primary else p.get("line",panel2))

        if isinstance(b, ctk.CTkButton):
            b.configure(
                fg_color=accent if primary else panel2,
                hover_color=accent2 if primary else hover,
                text_color="#ffffff" if primary else text,
                corner_radius=12,
                height=40 if primary else 38,
                border_width=0,
                font=("Segoe UI",12 if primary else 11,"bold" if primary else "normal")
            )
        else:
            b.configure(
                bg=accent if primary else panel2,
                fg="#ffffff" if primary else text,
                activebackground=accent2 if primary else hover,
                activeforeground="#ffffff" if primary else text,
                relief="flat", bd=0, padx=12, pady=7,
                cursor="hand2"
            )

    def card(self,parent):
        p=self.p()
        return ctk.CTkFrame(parent,fg_color=p["panel"],corner_radius=20,
                            border_width=1,border_color=p["line"])

    def _build_shell(self):
        p=self.p()
        self.root.configure(bg=p["bg"])
        try:
            st=ttk.Style()
            try: st.theme_use("clam")
            except Exception: pass
            st.configure("Horizontal.TProgressbar",troughcolor=p["entry"],background=p["accent2"],
                         bordercolor=p["line"],lightcolor=p["accent2"],darkcolor=p["accent"],thickness=10)
            st.configure("TCombobox",fieldbackground=p["entry"],background=p["panel2"],foreground=p["text"],
                         arrowcolor=p["accent2"],bordercolor=p["line"],lightcolor=p["panel2"],darkcolor=p["panel2"])
            st.map("TCombobox",fieldbackground=[("readonly",p["entry"])],foreground=[("readonly",p["text"])],
                   selectbackground=[("readonly",p["entry"])],selectforeground=[("readonly",p["text"])])
            self.root.option_add("*TCombobox*Listbox.background",p["entry"])
            self.root.option_add("*TCombobox*Listbox.foreground",p["text"])
            self.root.option_add("*TCombobox*Listbox.selectBackground",p["accent"])
        except Exception:
            pass

        self.sidebar=tk.Frame(self.root,bg=p["panel"],width=262)
        self.sidebar.pack(side="left",fill="y")
        self.sidebar.pack_propagate(False)

        brand=tk.Frame(self.sidebar,bg=p["panel"])
        brand.pack(fill="x",padx=18,pady=(22,18))
        try:
            _im=Image.open(resource_path("ATRAC_v30.ico")).convert("RGBA")
            self._brand_img=ctk.CTkImage(light_image=_im,dark_image=_im,size=(46,46))
            ctk.CTkLabel(brand,text="",image=self._brand_img,fg_color="transparent").pack(side="left")
        except Exception:
            tk.Label(brand,text="A",font=("Segoe UI",34,"bold"),bg=p["panel"],fg=p["accent2"]).pack(side="left")
        txt=tk.Frame(brand,bg=p["panel"]); txt.pack(side="left",padx=(8,0))
        tk.Label(txt,text="ATRAC",font=("Segoe UI",17,"bold"),bg=p["panel"],fg=p["text"]).pack(anchor="w")
        tk.Label(txt,text=self.tr("audio_studio"),font=("Segoe UI",8),bg=p["panel"],fg=p["muted"]).pack(anchor="w")

        # Dark mode was removed by request. Keep only language switching here.
        settings=tk.Frame(self.sidebar,bg=p["panel"])
        settings.pack(fill="x",padx=12,pady=(0,10))
        lang_text="ENGLISH" if self.lang=="ja" else "日本語"
        lb=tk.Button(settings,text=lang_text,command=self.toggle_language,
                     bg=p["panel2"],fg=p["text"],activebackground=p["accent"],
                     activeforeground="white",relief="flat",bd=0,cursor="hand2",
                     font=("Segoe UI",9,"bold"),padx=8,pady=6)
        lb.pack(side="left",fill="x",expand=True)

        # Scrollable navigation: generous spacing without cutting off lower tools.
        nav_canvas=tk.Canvas(self.sidebar,bg=p["panel"],highlightthickness=0,bd=0)
        nav_scroll=ttk.Scrollbar(self.sidebar,orient="vertical",command=nav_canvas.yview)
        nav_canvas.configure(yscrollcommand=nav_scroll.set)
        nav_scroll.pack(side="right",fill="y")
        nav_canvas.pack(side="left",fill="both",expand=True)
        nav_frame=tk.Frame(nav_canvas,bg=p["panel"])
        nav_window=nav_canvas.create_window((0,0),window=nav_frame,anchor="nw")
        nav_frame.bind("<Configure>",lambda e: nav_canvas.configure(scrollregion=nav_canvas.bbox("all")))
        nav_canvas.bind("<Configure>",lambda e: nav_canvas.itemconfigure(nav_window,width=e.width))
        def _nav_wheel(event):
            if event.delta:
                nav_canvas.yview_scroll(-int(event.delta/abs(event.delta)),"units")
            elif event.num in (4,5):
                nav_canvas.yview_scroll(-1 if event.num==4 else 1,"units")
        # Bind locally to navigation only, keeping page scroll behavior intact.
        for widget in (nav_canvas,nav_frame):
            widget.bind("<MouseWheel>",_nav_wheel)
            widget.bind("<Button-4>",_nav_wheel)
            widget.bind("<Button-5>",_nav_wheel)

        self.nav={}
        navs=[
            ("home", self.tr("home")),
            ("library", "▣  ローカルライブラリー" if self.lang=="ja" else "▣  Local Library"),
            ("convert", "♫  音楽・動画変換" if self.lang=="ja" else "♫  Audio / Video Convert"),
            ("video_compress", "▣  動画圧縮" if self.lang=="ja" else "▣  Video Compress"),
            ("audio_compress", "♫  音声圧縮" if self.lang=="ja" else "♫  Audio Compress"),
            ("image_compress", "▧  画像圧縮" if self.lang=="ja" else "▧  Image Compress"),
            ("car_at3", "💾  カロッツェリアAT3" if self.lang=="ja" else "💾  Carrozzeria AT3"),
            ("youtube", self.tr("youtube")),
            ("tiktok", self.tr("tiktok")),
            ("spotify", "●  Spotifyダウンロード" if self.lang=="ja" else "●  Spotify Download"),
            ("apple_music", "♪  Apple Musicダウンロード" if self.lang=="ja" else "♪  Apple Music Download"),
            ("youtube_music", "▶  YouTube Musicダウンロード" if self.lang=="ja" else "▶  YouTube Music Download"),
            ("mtime_editor", "🕒  フォルダー/ファイル 更新時間編集" if self.lang=="ja" else "🕒  File / Folder Modified Time"),
            ("batch", self.tr("batch")),
            ("batch_rename", "✎  一括フォルダー名編集" if self.lang=="ja" else "✎  Batch Folder Rename"),
            ("inner_rename", "♫  フォルダー内ファイル名" if self.lang=="ja" else "♫  Files Inside Folder"),
            ("universal", "▧  画像変換" if self.lang=="ja" else "▧  Image Convert"),
            ("gain", "🔊  音量調整" if self.lang=="ja" else "🔊  Volume"),
            ("format", self.tr("format")),
            ("calculator", self.tr("calculator")),
        ]
        for key,label in navs:
            b=ctk.CTkButton(nav_frame,text=label,anchor="w",command=lambda k=key:self.show_page(k),
                            fg_color="transparent",hover_color=p["hover"],text_color=p["text"],
                            corner_radius=11,height=42,border_width=0,font=("Segoe UI",12))
            b.pack(fill="x",padx=13,pady=3)
            b.bind("<MouseWheel>",_nav_wheel,add="+")
            self.nav[key]=b

        sep=tk.Frame(nav_frame,bg=p["line"],height=1); sep.pack(fill="x",padx=14,pady=12)
        tk.Label(nav_frame,text=self.tr("formats"),font=("Segoe UI",9,"bold"),bg=p["panel"],fg=p["muted"]).pack(anchor="w",padx=18)
        for s in ["MP3 / M4A / WAV","FLAC / ADTS","MP4 / MKV / WEBM / MOV"]:
            tk.Label(nav_frame,text=s,font=("Segoe UI",9),bg=p["panel"],fg=p["text"]).pack(anchor="w",padx=18,pady=2)

        right=tk.Frame(self.root,bg=p["bg"]); right.pack(side="left",fill="both",expand=True)
        self.topbar=tk.Frame(right,bg=p["bg"]); self.topbar.pack(fill="x",padx=24,pady=(18,10))
        tk.Label(self.topbar,text=self.tr("app"),font=("Segoe UI",20,"bold"),bg=p["bg"],fg=p["text"]).pack(side="left")

        # Dark mode removed: keep only the language switch in the top bar.
        top_lang=tk.Button(
            self.topbar,
            text=("ENGLISH" if self.lang=="ja" else "日本語"),
            command=self.toggle_language,
            bg=p["panel2"],fg=p["text"],
            activebackground=p["accent"],activeforeground="white",
            relief="flat",bd=0,cursor="hand2",
            font=("Segoe UI",9,"bold"),padx=12,pady=6
        )
        top_lang.pack(side="right")

        self.content=tk.Frame(right,bg=p["bg"]); self.content.pack(fill="both",expand=True,padx=24,pady=(0,22))

    def rebuild_shell(self):
        self._deferred_rebuild(getattr(self,"current_page","home"))

    def _deferred_rebuild(self, page=None):
        target = page or getattr(self,"current_page","home")
        def _do():
            try:
                # Hide instead of destroying live CustomTkinter widgets.
                # This avoids Tcl "invalid command name" errors during theme/language changes.
                for w in self.root.winfo_children():
                    try:
                        w.pack_forget()
                    except Exception:
                        try: w.grid_remove()
                        except Exception: pass
                self._build_shell()
                self.show_page(target if target in self.nav else "home")
            except Exception as e:
                try: messagebox.showerror(APP_NAME, f"UI rebuild error:\n{e}")
                except Exception: pass
        self.root.after_idle(_do)

    def toggle_theme(self):
        # Dark mode was removed. Keep the method for backward compatibility.
        self.theme="light"
        try:
            ctk.set_appearance_mode("Light")
        except Exception:
            pass

    def toggle_language(self):
        self.lang="en" if self.lang=="ja" else "ja"
        self._deferred_rebuild(getattr(self,"current_page","home"))

    def highlight(self,key):
        p=self.p()
        for k,b in self.nav.items():
            b.configure(fg_color=p["accent"] if k==key else "transparent",
                        hover_color=p["accent"] if k==key else p["hover"],
                        text_color="white" if k==key else p["text"])

    def _track_proc(self, proc):
        """Remember a long-running child so app close can kill it."""
        if not proc:
            return proc
        try:
            with self._tracked_procs_lock:
                self._tracked_procs.append(proc)
        except Exception:
            pass
        return proc

    def _untrack_proc(self, proc):
        try:
            with self._tracked_procs_lock:
                self._tracked_procs = [p for p in self._tracked_procs if p is not proc]
        except Exception:
            pass

    def _is_work_cancelled(self):
        try:
            if getattr(self, "_app_closing", False):
                return True
            if getattr(self, "_cancel_work", None) is not None and self._cancel_work.is_set():
                return True
        except Exception:
            pass
        return False

    def _stop_all_work(self):
        """Cancel downloads/conversions and kill tracked child processes."""
        self._app_closing=True
        try:
            self._cancel_work.set()
        except Exception:
            pass
        try:
            self.download_active=False
        except Exception:
            pass
        try:
            self.player_stop_requested=True
            self.player_gen = getattr(self, "player_gen", 0) + 1
        except Exception:
            pass
        # Copy list under lock, then kill outside the lock.
        try:
            with self._tracked_procs_lock:
                procs=list(self._tracked_procs)
                self._tracked_procs.clear()
        except Exception:
            procs=[]
        for proc in procs:
            try:
                self._kill_process(proc, timeout=1.0)
            except Exception:
                pass
        try:
            self._player_stop_proc()
        except Exception:
            pass
        try:
            self._video_preview_stop()
        except Exception:
            pass
        try:
            self._kill_helper_binaries()
        except Exception:
            pass

    def _on_app_close(self):
        """Stop every background job, then destroy the main window."""
        try:
            self._stop_all_work()
        except Exception:
            pass
        try:
            self.root.destroy()
        except Exception:
            try:
                self.root.quit()
            except Exception:
                pass

    def _kill_helper_binaries(self):
        """Best-effort kill of helper tools that may outlive tracked handles."""
        flags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
        if sys.platform == "win32":
            for title in ("ATRAC Player", "ATRAC 動画プレビュー"):
                try:
                    subprocess.run(
                        ["taskkill", "/F", "/FI", f"WINDOWTITLE eq {title}*"],
                        capture_output=True, creationflags=flags, timeout=5,
                    )
                except Exception:
                    pass
            # Kill helper executables that this app commonly launches.
            # Prefer process-tree kills so ffmpeg children of yt-dlp die too.
            for image in ("ffplay.exe", "yt-dlp.exe", "ffmpeg.exe", "ffprobe.exe", "deno.exe"):
                try:
                    subprocess.run(
                        ["taskkill", "/F", "/IM", image, "/T"],
                        capture_output=True, creationflags=flags, timeout=5,
                    )
                except Exception:
                    pass
        else:
            try:
                import signal
                patterns = [
                    r"ffplay.*(ATRAC Player|ATRAC 動画プレビュー)",
                    r"yt-dlp",
                    r"ffmpeg",
                    r"ffprobe",
                    r"deno",
                ]
                for pat in patterns:
                    for sig in (signal.SIGTERM, signal.SIGKILL):
                        try:
                            subprocess.run(
                                ["pkill", f"-{int(sig)}", "-P", str(os.getpid()), "-f", pat],
                                capture_output=True, timeout=3,
                            )
                        except Exception:
                            try:
                                subprocess.run(
                                    ["pkill", f"-{int(sig)}", "-f", pat],
                                    capture_output=True, timeout=3,
                                )
                            except Exception:
                                pass
            except Exception:
                pass

    def _kill_orphan_ffplay(self):
        """Compatibility wrapper used by older call sites."""
        self._kill_helper_binaries()

    def _svc_save_settings(self):
        """Remember each download page's own output settings."""
        svc=getattr(self,"service_active",None)
        if not svc:
            return
        try:
            self._svc_settings[svc]={
                "fmt":self.online_fmt.get(),"vq":self.video_quality.get(),
                "aq":self.audio_quality.get(),"sr":self.online_sample_rate.get(),
            }
        except Exception:
            pass

    def _svc_load_settings(self,svc,default_fmt,allowed,default_aq=None):
        """Restore this page's settings so other download pages do not overwrite them."""
        s=self._svc_settings.get(svc)
        fmt=(s or {}).get("fmt",default_fmt)
        if fmt not in allowed:
            fmt=default_fmt
        self.online_fmt.set(fmt)
        if s:
            for var,key in ((self.video_quality,"vq"),(self.audio_quality,"aq"),(self.online_sample_rate,"sr")):
                if s.get(key):
                    var.set(s[key])
        elif default_aq:
            self.audio_quality.set(default_aq)

    def show_page(self,key):
        # Preserve text entered on a streaming-service page before its widgets are destroyed.
        try:
            if getattr(self,"service_active",None) and getattr(self,"service_text_widget",None):
                self.service_urls[self.service_active]=self.service_text_widget.get("1.0","end-1c")
        except Exception:
            pass
        self._svc_save_settings()
        self.service_active=None
        self.service_text_widget=None
        self.current_page=key
        self.clear_content(); self.highlight(key)
        if key=="home": self.page_home()
        elif key=="library": self.page_library()
        elif key=="convert": self.page_convert()
        elif key=="video_compress": self.page_video_compress()
        elif key=="audio_compress": self.page_audio_compress()
        elif key=="image_compress": self.page_image_compress()
        elif key=="car_at3": self.page_carrozzeria_at3()
        elif key=="batch": self.open_batch_tags()
        elif key=="batch_rename": self.page_batch_rename()
        elif key=="inner_rename": self.page_inner_file_rename()
        elif key=="youtube": self.page_youtube()
        elif key=="tiktok": self.page_tiktok()
        elif key=="spotify": self.page_stream_service("spotify")
        elif key=="apple_music": self.page_stream_service("apple_music")
        elif key=="youtube_music": self.page_stream_service("youtube_music")
        elif key=="mtime_editor": self.page_mtime_editor()
        elif key=="universal": self.page_universal()
        elif key=="gain": self.page_gain()
        elif key=="format": self.page_format()
        elif key=="calculator": self.page_calculator()

    def page_home(self):
        p=self.p()

        hero_bg=p["panel"]
        hero=ctk.CTkFrame(self.content, fg_color=hero_bg, corner_radius=22)
        hero.pack(fill="x", pady=(0,18))
        h=tk.Frame(hero,bg=hero_bg)
        h.pack(fill="x", padx=28, pady=24)
        tk.Label(h,text="ATRAC Audio Video Converter",
                 font=("Segoe UI",28,"bold"),bg=hero_bg,fg=p["text"]).pack(anchor="w")
        subtitle=("音楽・動画・画像をもっと簡単に。ホームからすぐ使えるように整理しました。"
                  if self.lang=="ja" else
                  "Music, video and image tools — simplified and easier to launch from Home.")
        tk.Label(h,text=subtitle,font=("Segoe UI",12,"bold"),
                 bg=hero_bg,fg=p["accent"]).pack(anchor="w", pady=(6,0))

        cards=tk.Frame(self.content,bg=p["bg"])
        cards.pack(fill="both",expand=True)
        for col in range(3):
            cards.grid_columnconfigure(col, weight=1, uniform="homecards")

        items=[
            ("▣", "ローカルライブラリー" if self.lang=="ja" else "Local Library",
             "ダウンロード履歴・ローカル音楽・アプリ内再生" if self.lang=="ja" else "Downloads, local music and built-in playback", "library"),
            ("♫", "音楽・動画変換" if self.lang=="ja" else "Audio / Video Convert",
             "MP3 / WAV / M4A / FLAC / MP4 など" if self.lang=="ja" else "MP3 / WAV / M4A / FLAC / MP4 and more", "convert"),
            ("▣", "動画圧縮" if self.lang=="ja" else "Video Compress",
             "容量を小さくして保存" if self.lang=="ja" else "Reduce video file size", "video_compress"),
            ("💾", "カロッツェリアAT3" if self.lang=="ja" else "Carrozzeria AT3",
             "カロッツェリア録音AT3をMP3 / WAV / FLAC / M4Aへ" if self.lang=="ja" else "Convert Carrozzeria-recorded AT3 to MP3 / WAV / FLAC / M4A", "car_at3"),
            ("▶", "YouTubeダウンロード" if self.lang=="ja" else "YouTube Download",
             "動画・音声を保存" if self.lang=="ja" else "Save video or audio", "youtube"),
            ("▶", "YouTube Musicダウンロード" if self.lang=="ja" else "YouTube Music Download",
             "YouTube Music から保存" if self.lang=="ja" else "Download from YouTube Music", "youtube_music"),
            ("●", "Spotifyダウンロード" if self.lang=="ja" else "Spotify Download",
             "曲情報を解決して保存" if self.lang=="ja" else "Resolve track info and download", "spotify"),
            ("♪", "Apple Musicダウンロード" if self.lang=="ja" else "Apple Music Download",
             "曲情報を解決して保存" if self.lang=="ja" else "Resolve track info and download", "apple_music"),
            ("♪", "TikTokダウンロード" if self.lang=="ja" else "TikTok Download",
             "動画・音声を保存" if self.lang=="ja" else "Save video or audio", "tiktok"),
            ("▣", "一括タグ編集" if self.lang=="ja" else "Batch Tag Edit",
             "複数ファイルのタグ・カバーをまとめて編集" if self.lang=="ja" else "Edit tags and cover art in bulk", "batch"),
            ("✎", "一括フォルダー名編集" if self.lang=="ja" else "Batch Folder Rename",
             "フォルダー名だけ連番変更（中のファイルは触らない）" if self.lang=="ja" else "Rename folders only (files inside untouched)", "batch_rename"),
            ("♫", "フォルダー内ファイル名" if self.lang=="ja" else "Files Inside Folder",
             "フォルダーを指定して中のファイル名だけ連番変更" if self.lang=="ja" else "Rename only files inside selected folders", "inner_rename"),
            ("▧", "画像変換" if self.lang=="ja" else "Image Convert",
             "PNG / JPG / WEBP などを変換" if self.lang=="ja" else "Convert PNG / JPG / WEBP and more", "universal"),
            ("🔊", "音量調整" if self.lang=="ja" else "Volume",
             "MP3 / MP4 などを一括調整" if self.lang=="ja" else "Batch-adjust MP3 / MP4 and more", "gain"),
            ("▦", "電卓" if self.lang=="ja" else "Calculator",
             "アプリ内のシンプル電卓" if self.lang=="ja" else "Simple built-in calculator", "calculator"),
        ]
        service_icon_keys={"youtube_music","youtube","spotify","tiktok","apple_music","car_at3"}
        strong_keys={"convert","car_at3","youtube","youtube_music","spotify","apple_music","tiktok"}

        for i,(ico,title,desc,key) in enumerate(items):
            r,c=divmod(i,3)
            card=ctk.CTkFrame(cards, fg_color=p["panel"], corner_radius=18,
                              border_width=1, border_color=p["line"])
            card.grid(row=r,column=c,sticky="nsew",padx=(0 if c==0 else 8, 0 if c==2 else 8),pady=(0,12))
            inner=tk.Frame(card,bg=p["panel"])
            inner.pack(fill="both",expand=True,padx=18,pady=18)
            ibg=p["panel2"]

            icon_widget=None
            if key in service_icon_keys:
                icon_image=self._get_home_icon(key,(50,50))
                if icon_image is not None:
                    icon_widget=ctk.CTkLabel(inner,text="",image=icon_image,fg_color=ibg,
                                             corner_radius=14,width=68,height=68)
                    icon_widget.pack(side="left",padx=(0,14))
            if icon_widget is None:
                icon=tk.Label(inner,text=ico,font=("Segoe UI",22,"bold"),width=3,height=1,
                              bg=ibg,fg="white" if key in strong_keys else p["accent"])
                icon.pack(side="left",padx=(0,14))
                icon_widget=icon

            text_frame=tk.Frame(inner,bg=p["panel"])
            text_frame.pack(side="left",fill="both",expand=True)
            tk.Label(text_frame,text=title,font=("Segoe UI",13,"bold"),bg=p["panel"],fg=p["text"]).pack(anchor="w")
            tk.Label(text_frame,text=desc,font=("Segoe UI",9),wraplength=245,justify="left",
                     bg=p["panel"],fg=p["muted"]).pack(anchor="w",pady=(5,0))
            for w in (card, inner, icon_widget, text_frame):
                try:
                    w.bind("<Button-1>", lambda e,k=key:self.show_page(k))
                except Exception:
                    pass
            for w in text_frame.winfo_children():
                w.bind("<Button-1>", lambda e,k=key:self.show_page(k))

        foot=tk.Label(self.content,
            text=("※ ダークモードは削除し、ホームに YouTube Music / YouTube / Spotify / TikTok / Apple Music / カロッツェリアAT3 を追加しました。"
                  if self.lang=="ja" else
                  "Dark mode was removed, and Home now includes YouTube Music / YouTube / Spotify / TikTok / Apple Music / Carrozzeria AT3."),
            font=("Segoe UI",8), bg=p["bg"], fg=p["muted"])
        foot.pack(anchor="w", pady=(2,8))

    # ------------------------------------------------------------------
    # Local Library
    # ------------------------------------------------------------------
    def _library_root(self):
        # Keep user media out of Program Files: installed apps normally cannot
        # write there without elevation.  This path works on Windows and macOS.
        return os.path.join(os.path.expanduser("~"), "Music", "ATRAC Library")

    def _library_download_dir(self):
        p=os.path.join(self._library_root(), "Downloads")
        os.makedirs(p, exist_ok=True)
        return p

    def _library_local_dir(self):
        p=os.path.join(self._library_root(), "Local Music")
        os.makedirs(p, exist_ok=True)
        return p

    def _ensure_library_dirs(self):
        try:
            os.makedirs(self._library_root(), exist_ok=True)
            os.makedirs(self._library_download_dir(), exist_ok=True)
            os.makedirs(self._library_local_dir(), exist_ok=True)
        except Exception:
            pass

    def _library_supported(self, path):
        return os.path.splitext(path)[1].lower() in {
            ".mp3",".m4a",".aac",".adts",".flac",".wav",".ogg",".opus",".wma",
            ".mp4",".mkv",".webm",".mov",".avi",".wmv",".m4v",".mpeg",".mpg"
        }

    def _library_kind(self, path):
        ext=os.path.splitext(path)[1].lower()
        return "動画" if ext in {".mp4",".mkv",".webm",".mov",".avi",".wmv",".m4v",".mpeg",".mpg"} else "音楽"

    def _library_meta(self, path):
        stem=os.path.splitext(os.path.basename(path))[0]
        try:
            st=os.stat(path)
            sig=(getattr(st,"st_mtime_ns",int(st.st_mtime*1e9)),st.st_size)
        except Exception:
            st=None; sig=(0,0)
        cached=self._library_meta_cache.get(path)
        if cached and cached[0]==sig:
            return dict(cached[1])
        title,artist,album=stem,"",""
        try:
            fp=tool("ffprobe")
            if fp:
                t=read_tags(fp,path)
                title=t.get("title") or stem
                artist=t.get("artist") or t.get("album_artist") or ""
                album=t.get("album") or ""
        except Exception:
            pass
        size=(st.st_size if st else 0)
        mtime=(st.st_mtime if st else 0)
        root=os.path.abspath(self._library_download_dir())
        src="ダウンロード" if os.path.abspath(path).startswith(root+os.sep) or os.path.abspath(path)==root else "ローカル"
        data={"path":path,"title":title,"artist":artist,"album":album,"kind":self._library_kind(path),"source":src,"size":size,"mtime":mtime}
        self._library_meta_cache[path]=(sig,dict(data))
        return data

    def _library_scan(self):
        self._ensure_library_dirs()
        out=[]
        for base in (self._library_download_dir(), self._library_local_dir()):
            for root,dirs,files in os.walk(base):
                for n in files:
                    path=os.path.join(root,n)
                    if self._library_supported(path):
                        out.append(self._library_meta(path))
        self.library_items=out
        return out

    def _library_unique_dest(self, folder, name):
        os.makedirs(folder, exist_ok=True)
        stem,ext=os.path.splitext(name)
        dest=os.path.join(folder,name)
        i=2
        while os.path.exists(dest):
            dest=os.path.join(folder,f"{stem} ({i}){ext}")
            i+=1
        return dest

    def _library_add_files(self):
        paths=filedialog.askopenfilenames(
            title="ローカル音楽を追加" if self.lang=="ja" else "Add Local Music",
            filetypes=[("Media","*.mp3 *.m4a *.aac *.adts *.flac *.wav *.ogg *.opus *.wma *.mp4 *.mkv *.webm *.mov *.avi *.wmv"),("All","*.*")]
        )
        if not paths:return
        paths=list(paths)
        dst=self._library_local_dir()
        self.library_status.set((f"{len(paths)}件を追加中..." if self.lang=="ja" else f"Adding {len(paths)} item(s)..."))
        def worker():
            added=0; errors=[]
            for src in paths:
                if not self._library_supported(src): continue
                try:
                    dest=self._library_unique_dest(dst,os.path.basename(src))
                    shutil.copy2(src,dest)
                    added+=1
                except Exception as e:
                    errors.append(f"{os.path.basename(src)}: {e}")
            def done():
                self._library_refresh()
                self.library_status.set((f"{added}件追加しました" if self.lang=="ja" else f"Added {added} item(s)"))
                if errors:
                    messagebox.showwarning(APP_NAME,("一部のファイルを追加できませんでした。\n" if self.lang=="ja" else "Some files could not be added.\n")+"\n".join(errors[:8]))
            try:self.root.after(0,done)
            except Exception:pass
        threading.Thread(target=worker,daemon=True).start()

    def _library_add_folder(self):
        src=filedialog.askdirectory(title="音楽フォルダを追加" if self.lang=="ja" else "Add Media Folder")
        if not src:return
        base_name=_sanitize_output_folder_name(os.path.basename(os.path.normpath(src)) or "Imported")
        local_root=self._library_local_dir()
        candidate=os.path.join(local_root,base_name); i=2
        while os.path.exists(candidate):
            candidate=os.path.join(local_root,f"{base_name} ({i})"); i+=1
        dst_root=candidate
        self.library_status.set(("フォルダを追加中..." if self.lang=="ja" else "Adding folder..."))
        def worker():
            added=0; errors=[]
            for root,dirs,files in os.walk(src):
                rel=os.path.relpath(root,src)
                target=dst_root if rel=="." else os.path.join(dst_root,rel)
                for n in files:
                    path=os.path.join(root,n)
                    if not self._library_supported(path): continue
                    try:
                        os.makedirs(target,exist_ok=True)
                        shutil.copy2(path,self._library_unique_dest(target,n)); added+=1
                    except Exception as e:
                        errors.append(f"{n}: {e}")
            def done():
                self._library_refresh()
                self.library_status.set((f"{added}件追加しました" if self.lang=="ja" else f"Added {added} item(s)"))
                if errors:
                    messagebox.showwarning(APP_NAME,("一部のファイルを追加できませんでした。\n" if self.lang=="ja" else "Some files could not be added.\n")+"\n".join(errors[:8]))
            try:self.root.after(0,done)
            except Exception:pass
        threading.Thread(target=worker,daemon=True).start()

    def _library_open_root(self):
        path=self._library_root(); self._ensure_library_dirs()
        try:
            if sys.platform=="win32": os.startfile(path)
            elif sys.platform=="darwin": subprocess.Popen(["open",path])
            else: subprocess.Popen(["xdg-open",path])
        except Exception as e: messagebox.showerror(APP_NAME,str(e))

    def _library_selected(self):
        if not hasattr(self,"library_tree"): return []
        out=[]
        for iid in self.library_tree.selection():
            try:
                idx=int(iid)
                if 0 <= idx < len(self.library_view_items): out.append(self.library_view_items[idx])
            except Exception: pass
        return out

    def _library_open_selected_location(self):
        rows=self._library_selected()
        if not rows:return
        path=rows[0]["path"]
        try:
            if sys.platform=="win32": subprocess.Popen(["explorer","/select,",os.path.normpath(path)])
            elif sys.platform=="darwin": subprocess.Popen(["open","-R",path])
            else: subprocess.Popen(["xdg-open",os.path.dirname(path)])
        except Exception as e: messagebox.showerror(APP_NAME,str(e))

    def _library_select_all(self,event=None):
        try:
            if self.library_tree is not None and self.library_tree.winfo_exists():
                self.library_tree.selection_set(self.library_tree.get_children())
        except Exception:
            pass
        return "break"

    def _library_delete_selected(self,event=None):
        rows=self._library_selected()
        if not rows:return "break"
        msg=(f"選択した{len(rows)}件をライブラリーとディスクから削除しますか？" if self.lang=="ja" else f"Delete {len(rows)} selected item(s) from the library and disk?")
        if not messagebox.askyesno(APP_NAME,msg): return "break"
        paths=[x["path"] for x in rows]
        self.library_status.set((f"{len(paths)}件を削除中..." if self.lang=="ja" else f"Deleting {len(paths)} item(s)..."))
        def worker():
            deleted=0; errors=[]
            for path in paths:
                try:
                    os.remove(path); deleted+=1
                    self._library_meta_cache.pop(path,None)
                except Exception as e:
                    errors.append(f"{os.path.basename(path)}: {e}")
            def done():
                self._library_refresh()
                self.library_status.set((f"{deleted}件削除しました" if self.lang=="ja" else f"Deleted {deleted} item(s)"))
                if errors:
                    messagebox.showwarning(APP_NAME,("一部を削除できませんでした。\n" if self.lang=="ja" else "Some items could not be deleted.\n")+"\n".join(errors[:8]))
            try:self.root.after(0,done)
            except Exception:pass
        threading.Thread(target=worker,daemon=True).start()
        return "break"

    def _library_open_cd_app(self):
        try:
            if sys.platform=="win32":
                candidates=[]
                for env_name in ("ProgramFiles(x86)","ProgramFiles"):
                    base=os.environ.get(env_name)
                    if base:
                        candidates.append(os.path.join(base,"Windows Media Player","wmplayer.exe"))
                found=shutil.which("wmplayer.exe")
                if found:candidates.append(found)
                for exe in candidates:
                    if exe and os.path.exists(exe):
                        subprocess.Popen([exe],creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
                        return
                # Windows 11 may only have the newer Media Player app.
                try:
                    os.startfile("mswindowsmusic:")
                    return
                except Exception:
                    pass
                subprocess.Popen(["explorer.exe","shell:AppsFolder\\Microsoft.ZuneMusic_8wekyb3d8bbwe!Microsoft.ZuneMusic"])
            elif sys.platform=="darwin":
                subprocess.Popen(["open","-a","Music"])
            else:
                messagebox.showinfo(APP_NAME,"CD書き込みアプリはWindows / macOSで開けます。" if self.lang=="ja" else "CD app launch is available on Windows / macOS.")
        except Exception as e:
            messagebox.showerror(APP_NAME,("Windows Media Player / Media Player を起動できませんでした。\n" if self.lang=="ja" else "Could not launch Windows Media Player / Media Player.\n")+str(e))

    def _library_play_selected(self, event=None):
        rows=self._library_selected()
        if not rows:return
        visible=[x["path"] for x in self.library_view_items if os.path.exists(x["path"])]
        self.player_files=visible
        try:self.player_index=visible.index(rows[0]["path"])
        except Exception:self.player_index=0
        self._player_play()
        self.library_current_path=rows[0]["path"]
        self._library_update_nowplaying()

    def _library_update_nowplaying(self):
        if not hasattr(self,"library_now_title"): return
        if self.player_files and 0 <= self.player_index < len(self.player_files):
            path=self.player_files[self.player_index]
            meta=self._library_meta(path)
            self.library_now_title.set(meta["title"])
            self.library_now_sub.set(" • ".join([x for x in (meta["artist"],meta["album"]) if x]) or os.path.basename(path))
        else:
            self.library_now_title.set("再生する曲を選択" if self.lang=="ja" else "Choose a track")
            self.library_now_sub.set("")

    def _library_prev(self):
        self._player_prev(); self.root.after(100,self._library_update_nowplaying)

    def _library_next(self):
        self._player_next(); self.root.after(100,self._library_update_nowplaying)

    def _library_toggle_play(self):
        if self.player_proc and self.player_proc.poll() is None:
            self._player_pause()
        elif self.player_paused:
            self._player_play(start_at=self.player_seek_offset)
        elif self.player_files:
            self._player_play()
        else:
            self._library_play_selected()
        self.root.after(100,self._library_update_nowplaying)

    def _library_refresh(self,*_):
        if not hasattr(self,"library_tree"):
            return
        try:
            q=(self.library_search.get() or "").strip().lower()
            flt=self.library_filter.get()
            sort=self.library_sort.get()
        except Exception:
            return
        self._library_refresh_token+=1
        token=self._library_refresh_token
        try:
            if self._library_refresh_after is not None:
                self.root.after_cancel(self._library_refresh_after)
        except Exception:
            pass
        try:self.library_status.set("読み込み中..." if self.lang=="ja" else "Loading...")
        except Exception:pass

        def launch():
            def worker():
                try:
                    items=self._library_scan()
                    if flt in ("音楽","Music"): items=[x for x in items if x["kind"]=="音楽"]
                    elif flt in ("動画","Video"): items=[x for x in items if x["kind"]=="動画"]
                    elif flt in ("ダウンロード","Downloads"): items=[x for x in items if x["source"]=="ダウンロード"]
                    elif flt in ("ローカル","Local"): items=[x for x in items if x["source"]=="ローカル"]
                    if q:
                        items=[x for x in items if q in " ".join((x["title"],x["artist"],x["album"],os.path.basename(x["path"]))).lower()]
                    if sort in ("タイトル","Title"): items.sort(key=lambda x:x["title"].lower())
                    elif sort in ("アーティスト","Artist"): items.sort(key=lambda x:x["artist"].lower())
                    elif sort in ("アルバム","Album"): items.sort(key=lambda x:x["album"].lower())
                    else: items.sort(key=lambda x:x["mtime"], reverse=True)
                except Exception as e:
                    items=[]
                def apply():
                    if token!=self._library_refresh_token:return
                    try:
                        if self.library_tree is None or not self.library_tree.winfo_exists():return
                    except Exception:
                        return
                    self.library_view_items=items
                    try:self.library_tree.delete(*self.library_tree.get_children())
                    except Exception:return
                    for i,x in enumerate(items):
                        size=x["size"]
                        if size>=1024**3: ss=f"{size/1024**3:.1f} GB"
                        elif size>=1024**2: ss=f"{size/1024**2:.1f} MB"
                        else: ss=f"{size/1024:.0f} KB"
                        try:self.library_tree.insert("","end",iid=str(i),values=(x["title"],x["artist"],x["album"],x["kind"],x["source"],ss))
                        except Exception:break
                    try:self.library_status.set((f"{len(items)}件" if self.lang=="ja" else f"{len(items)} item(s)"))
                    except Exception:pass
                try:self.root.after(0,apply)
                except Exception:pass
            threading.Thread(target=worker,daemon=True).start()
        try:
            self._library_refresh_after=self.root.after(120,launch)
        except Exception:
            launch()

    def page_library(self):
        p=self.p()
        # Header — intentionally spacious and simple, like TuneFab Local Library.
        head=tk.Frame(self.content,bg=p["bg"]); head.pack(fill="x",pady=(2,14))
        left=tk.Frame(head,bg=p["bg"]); left.pack(side="left")
        tk.Label(left,text="ローカルライブラリー" if self.lang=="ja" else "Local Library",font=("Segoe UI",24,"bold"),bg=p["bg"],fg=p["text"]).pack(anchor="w")
        tk.Label(left,text="ダウンロード済みとローカルの音楽・動画" if self.lang=="ja" else "Downloaded and local music & video",font=("Segoe UI",10),bg=p["bg"],fg=p["muted"]).pack(anchor="w",pady=(3,0))
        actions=tk.Frame(head,bg=p["bg"]); actions.pack(side="right")
        for text_,cmd,primary in [
            ("＋ ローカル音楽を追加" if self.lang=="ja" else "+ Add Local Music",self._library_add_files,True),
            ("フォルダ追加" if self.lang=="ja" else "Add Folder",self._library_add_folder,False),
            ("ライブラリーファイルを開く" if self.lang=="ja" else "Open Library Folder",self._library_open_root,False),
        ]:
            b=ctk.CTkButton(actions,text=text_,command=cmd); self.style_button(b,primary); b.pack(side="left",padx=(8,0))

        # Main card
        c=self.card(self.content); c.pack(fill="both",expand=True)
        toolbar=tk.Frame(c,bg=p["panel"]); toolbar.pack(fill="x",padx=18,pady=(16,10))
        search=ctk.CTkEntry(toolbar,textvariable=self.library_search,placeholder_text="検索" if self.lang=="ja" else "Search",width=300,height=36,corner_radius=10)
        search.pack(side="left")
        search.bind("<KeyRelease>",self._library_refresh)
        filters=["すべて","音楽","動画","ダウンロード","ローカル"] if self.lang=="ja" else ["All","Music","Video","Downloads","Local"]
        if self.library_filter.get() not in filters:self.library_filter.set(filters[0])
        fbox=ctk.CTkComboBox(toolbar,values=filters,variable=self.library_filter,width=140,command=self._library_refresh,corner_radius=10)
        fbox.pack(side="left",padx=(10,0))
        sorts=["追加日時","タイトル","アーティスト","アルバム"] if self.lang=="ja" else ["Added","Title","Artist","Album"]
        if self.library_sort.get() not in sorts:self.library_sort.set(sorts[0])
        sbox=ctk.CTkComboBox(toolbar,values=sorts,variable=self.library_sort,width=150,command=self._library_refresh,corner_radius=10)
        sbox.pack(side="left",padx=(10,0))
        tk.Label(toolbar,textvariable=self.library_status,bg=p["panel"],fg=p["muted"],font=("Segoe UI",9)).pack(side="right")

        table=tk.Frame(c,bg=p["panel"]); table.pack(fill="both",expand=True,padx=18,pady=(0,10))
        style=ttk.Style()
        try:
            style.configure("ATRAC.Treeview",rowheight=34,font=("Segoe UI",10),background=p["entry"],fieldbackground=p["entry"],foreground=p["text"],borderwidth=0)
            style.configure("ATRAC.Treeview.Heading",font=("Segoe UI",9,"bold"))
            style.map("ATRAC.Treeview",background=[("selected",p["accent"])],foreground=[("selected","white")])
        except Exception: pass
        cols=("title","artist","album","kind","source","size")
        self.library_tree=ttk.Treeview(table,columns=cols,show="headings",style="ATRAC.Treeview",selectmode="extended")
        heads=[("title","タイトル" if self.lang=="ja" else "Title",260),("artist","アーティスト" if self.lang=="ja" else "Artist",160),("album","アルバム" if self.lang=="ja" else "Album",180),("kind","種類" if self.lang=="ja" else "Type",70),("source","場所" if self.lang=="ja" else "Source",100),("size","サイズ" if self.lang=="ja" else "Size",80)]
        for key,label,w in heads:
            self.library_tree.heading(key,text=label); self.library_tree.column(key,width=w,minwidth=60,anchor="w")
        vs=ttk.Scrollbar(table,orient="vertical",command=self.library_tree.yview); self.library_tree.configure(yscrollcommand=vs.set)
        self.library_tree.pack(side="left",fill="both",expand=True); vs.pack(side="right",fill="y")
        self.library_tree.bind("<Double-Button-1>",self._library_play_selected)
        self.library_tree.bind("<Control-a>",self._library_select_all)
        self.library_tree.bind("<Control-A>",self._library_select_all)
        self.library_tree.bind("<Delete>",self._library_delete_selected)

        # File actions
        fr=tk.Frame(c,bg=p["panel"]); fr.pack(fill="x",padx=18,pady=(0,10))
        for txt,cmd in [
            ("▶ 再生" if self.lang=="ja" else "▶ Play",self._library_play_selected),
            ("全選択" if self.lang=="ja" else "Select All",self._library_select_all),
            ("選択を削除" if self.lang=="ja" else "Delete Selected",self._library_delete_selected),
            ("ファイルの場所を開く" if self.lang=="ja" else "Open File Location",self._library_open_selected_location),
            ("CD書き込み用アプリを開く" if self.lang=="ja" else "Open CD Burning App",self._library_open_cd_app),
        ]:
            b=ctk.CTkButton(fr,text=txt,command=cmd); self.style_button(b,txt.startswith("▶")); b.pack(side="left",padx=(0,8))

        # Persistent-style bottom player bar inside library page.
        player=ctk.CTkFrame(c,fg_color=p["panel2"],corner_radius=14)
        player.pack(fill="x",padx=18,pady=(0,16))
        self.library_now_title=tk.StringVar(value="再生する曲を選択" if self.lang=="ja" else "Choose a track")
        self.library_now_sub=tk.StringVar(value="")
        info=tk.Frame(player,bg=p["panel2"]); info.pack(side="left",fill="x",expand=True,padx=16,pady=12)
        tk.Label(info,textvariable=self.library_now_title,bg=p["panel2"],fg=p["text"],font=("Segoe UI",11,"bold")).pack(anchor="w")
        tk.Label(info,textvariable=self.library_now_sub,bg=p["panel2"],fg=p["muted"],font=("Segoe UI",8)).pack(anchor="w")
        ctrl=tk.Frame(player,bg=p["panel2"]); ctrl.pack(side="right",padx=12)
        for txt,cmd in [("◀",self._library_prev),("▶ / Ⅱ",self._library_toggle_play),("■",self._player_stop),("▶",self._library_next)]:
            b=ctk.CTkButton(ctrl,text=txt,command=cmd,width=58,height=34,corner_radius=17,fg_color=p["accent"] if "Ⅱ" in txt else p["panel"],hover_color=p["accent2"])
            b.pack(side="left",padx=3)
        tk.Label(ctrl,text="音量" if self.lang=="ja" else "Vol",bg=p["panel2"],fg=p["muted"],font=("Segoe UI",8)).pack(side="left",padx=(10,3))
        ttk.Scale(ctrl,from_=0,to=100,variable=self.player_vol,orient="horizontal",length=90,
                  command=self._player_vol_changed).pack(side="left")
        seek=tk.Frame(c,bg=p["panel"]); seek.pack(fill="x",padx=18,pady=(0,12))
        self.player_seek=ttk.Scale(seek,from_=0,to=1000,orient="horizontal",variable=self.player_pos,command=self._player_on_seek_drag)
        self.player_seek.pack(side="left",fill="x",expand=True)
        self.player_seek.bind("<ButtonPress-1>",lambda e:setattr(self,"player_seeking",True))
        self.player_seek.bind("<ButtonRelease-1>",self._player_on_seek_release)
        tk.Label(seek,textvariable=self.player_time_label,bg=p["panel"],fg=p["muted"],font=("Segoe UI",8),width=13).pack(side="left",padx=(8,0))
        self._library_refresh()
        self._library_update_nowplaying()

    def page_convert(self):
        p=self.p()

        top=self.card(self.content)
        top.pack(fill="x",pady=(0,12))

        hdr=tk.Frame(top,bg=p["panel"])
        hdr.pack(fill="x",padx=18,pady=14)

        tk.Label(
            hdr,
            text=self.tr("audio_convert"),
            font=("Segoe UI",16,"bold"),
            bg=p["panel"],
            fg=p["text"]
        ).pack(side="left")

        folder_btn=ctk.CTkButton(hdr,text=("+ フォルダー追加" if self.lang=="ja" else "+ Add Folder"),command=self.add_convert_folder)
        self.style_button(folder_btn)
        folder_btn.pack(side="right",padx=(0,8))

        b=ctk.CTkButton(hdr,text=self.tr("+add"),command=self.add_files)
        self.style_button(b,True)
        b.pack(side="right")

        b2=ctk.CTkButton(hdr,text=self.tr("clear"),command=self.clear_files)
        self.style_button(b2)
        b2.pack(side="right",padx=(0,8))

        b3=ctk.CTkButton(hdr,text=self.tr("remove"),command=self.remove_selected)
        self.style_button(b3)
        b3.pack(side="right",padx=(0,8))

        body=self.card(self.content)
        body.pack(fill="both",expand=True)

        opts=tk.Frame(body,bg=p["panel"])
        opts.pack(fill="x",padx=16,pady=12)

        tk.Label(
            opts,
            text=self.tr("output"),
            bg=p["panel"],
            fg=p["text"],
            font=("Segoe UI",10,"bold")
        ).pack(side="left")

        ttk.Combobox(
            opts,
            textvariable=self.outfmt,
            state="readonly",
            values=[
                "WAV",
                "MP3",
                "M4A",
                "OPUS",
                "FLAC",
                "ADTS (.adts)",
                "MP4 (H.264/AAC)",
                "MKV (H.264/AAC)",
                "WEBM (VP9/Opus)",
                "MOV (H.264/AAC)"
            ],
            width=19
        ).pack(side="left",padx=(8,18))

        tk.Label(
            opts,
            text=self.tr("bitrate"),
            bg=p["panel"],
            fg=p["text"],
            font=("Segoe UI",10,"bold")
        ).pack(side="left")

        ttk.Combobox(
            opts,
            textvariable=self.bitrate,
            state="readonly",
            values=["64k","96k","128k","160k","192k","256k","320k"],
            width=9
        ).pack(side="left",padx=(8,12))

        tk.Label(
            opts,
            text="サンプルレート" if self.lang=="ja" else "Sample Rate",
            bg=p["panel"],
            fg=p["text"],
            font=("Segoe UI",10,"bold")
        ).pack(side="left")

        ttk.Combobox(
            opts,
            textvariable=self.sample_rate,
            state="readonly",
            values=["元のまま","22050","32000","44100","48000","96000"],
            width=10
        ).pack(side="left",padx=(8,12))

        fmtbtn=ctk.CTkButton(
            opts,
            text="拡張子・形式変換",
            command=lambda:self.show_page("universal")
        )
        self.style_button(fmtbtn)
        fmtbtn.pack(side="right")

        delete_row=tk.Frame(body,bg=p["panel"])
        delete_row.pack(fill="x",padx=16,pady=(0,10))
        ctk.CTkCheckBox(
            delete_row,
            text="変換成功後に元のファイルを削除する",
            variable=self.delete_source_after_convert,
            onvalue=True,
            offvalue=False
        ).pack(side="left")
        tk.Label(
            delete_row,
            text="※ OFFが初期設定。成功したファイルだけ削除します。",
            bg=p["panel"],
            fg=p["muted"],
            font=("Segoe UI",9)
        ).pack(side="left",padx=(10,0))

        self.listbox=tk.Listbox(
            body,
            selectmode="extended",
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=("Segoe UI",10),
            bg=p["panel2"],
            fg=p["text"],
            selectbackground=p["accent"]
        )
        self.listbox.pack(fill="both",expand=True,padx=16,pady=(0,12))
        self._enable_drop(self.listbox,self._add_convert_dropped)

        for f in self.files:
            self.listbox.insert("end",f)

        bottom=tk.Frame(body,bg=p["panel"])
        bottom.pack(fill="x",padx=16,pady=(0,16))

        self.convprog=ttk.Progressbar(bottom,maximum=100)
        self.convprog.pack(side="left",fill="x",expand=True,padx=(0,8))

        self.convpercent=tk.Label(
            bottom,
            text="0%",
            width=5,
            bg=p["panel"],
            fg=p["text"],
            font=("Segoe UI",10,"bold")
        )
        self.convpercent.pack(side="left",padx=(0,12))

        b=ctk.CTkButton(bottom,text=self.tr("start"),command=self.do_convert)
        self.convert_start_button=b
        self.style_button(b,True)
        b.pack(side="right")
        self._add_cancel_button(bottom,command=self.cancel_operation,enabled=getattr(self,"_convert_running",False))


    def page_video_compress(self):
        p=self.p()
        top=self.card(self.content)
        top.pack(fill="x",pady=(0,12))
        hdr=tk.Frame(top,bg=p["panel"])
        hdr.pack(fill="x",padx=18,pady=14)
        tk.Label(hdr,text=("動画圧縮" if self.lang=="ja" else "Video Compress"),
                 font=("Segoe UI",16,"bold"),bg=p["panel"],fg=p["text"]).pack(side="left")

        def add_files():
            fs=filedialog.askopenfilenames(filetypes=[
                ("Video","*.mp4 *.mkv *.mov *.webm *.avi *.m4v *.ts *.mpg *.mpeg"),
                ("All","*.*")
            ])
            self._video_compress_add(fs)

        for label,cmd,primary in [
            (("+ 動画追加" if self.lang=="ja" else "+ Add Video"),add_files,True),
            (("選択削除" if self.lang=="ja" else "Remove Selected"),self._video_compress_remove,False),
            (("全消去" if self.lang=="ja" else "Clear All"),self._video_compress_clear,False),
        ]:
            b=ctk.CTkButton(hdr,text=label,command=cmd); self.style_button(b,primary)
            b.pack(side="right",padx=(8,0))

        body=self.card(self.content)
        body.pack(fill="both",expand=True)

        self.video_compress_list=tk.Listbox(
            body,selectmode="extended",relief="flat",bd=0,highlightthickness=0,
            font=("Segoe UI",10),bg=p["panel2"],fg=p["text"],selectbackground=p["accent"]
        )
        self.video_compress_list.pack(fill="both",expand=True,padx=16,pady=(16,12))
        for f in self.video_compress_files:
            self.video_compress_list.insert("end",f)
        self._enable_drop(self.video_compress_list,self._video_compress_add)

        opts=tk.Frame(body,bg=p["panel"])
        opts.pack(fill="x",padx=16,pady=(0,8))

        tk.Label(opts,text=("圧縮率" if self.lang=="ja" else "Compression"),
                 bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")).pack(side="left")
        ttk.Combobox(opts,textvariable=self.video_compress_quality,state="readonly",
                     values=["高画質","標準","強く圧縮"],width=12).pack(side="left",padx=(8,16))

        tk.Label(opts,text=("解像度" if self.lang=="ja" else "Resolution"),
                 bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")).pack(side="left")
        ttk.Combobox(opts,textvariable=self.video_compress_resolution,state="readonly",
                     values=["元のまま","1080p","720p","480p"],width=12).pack(side="left",padx=(8,16))

        tk.Label(opts,text=("音声" if self.lang=="ja" else "Audio"),
                 bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")).pack(side="left")
        ttk.Combobox(opts,textvariable=self.video_compress_audio_bitrate,state="readonly",
                     values=["96k","128k","160k","192k","256k"],width=8).pack(side="left",padx=(8,16))

        tk.Label(opts,text=("速度" if self.lang=="ja" else "Speed"),
                 bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")).pack(side="left")
        ttk.Combobox(opts,textvariable=self.video_compress_speed,state="readonly",
                     values=["最速","高速","標準","高圧縮"],width=8).pack(side="left",padx=(8,16))

        tk.Label(opts,text=("保存先" if self.lang=="ja" else "Output"),
                 bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")).pack(side="left")
        tk.Entry(opts,textvariable=self.video_compress_outdir,bg=p["entry"],fg=p["text"],
                 insertbackground=p["text"],relief="flat",bd=0).pack(side="left",fill="x",expand=True,padx=8,ipady=7)
        b=ctk.CTkButton(opts,text=("参照" if self.lang=="ja" else "Browse"),
                        command=lambda:self._choose_dir_var(self.video_compress_outdir))
        self.style_button(b); b.pack(side="left")

        delrow=tk.Frame(body,bg=p["panel"])
        delrow.pack(fill="x",padx=16,pady=(0,8))
        ctk.CTkCheckBox(
            delrow,
            text=("圧縮成功後に元の動画を削除する" if self.lang=="ja" else "Delete source after successful compression"),
            variable=self.video_compress_delete_source,onvalue=True,offvalue=False
        ).pack(side="left")

        prog=tk.Frame(body,bg=p["panel"])
        prog.pack(fill="x",padx=16,pady=(4,16))
        self.video_compress_progress=ttk.Progressbar(prog,maximum=100)
        self.video_compress_progress.pack(side="left",fill="x",expand=True,padx=(0,8))
        self.video_compress_percent=tk.Label(prog,text="0%",width=5,bg=p["panel"],fg=p["text"],
                                             font=("Segoe UI",10,"bold"))
        self.video_compress_percent.pack(side="left",padx=(0,12))
        b=ctk.CTkButton(prog,text=("圧縮開始" if self.lang=="ja" else "Start Compress"),
                        command=self._video_compress_start)
        self.video_compress_start_button=b
        self.style_button(b,True); b.pack(side="right")
        self._add_cancel_button(prog,command=self.cancel_operation,enabled=self.video_compress_busy)

    def _video_compress_add(self,paths):
        allowed={".mp4",".mkv",".mov",".webm",".avi",".m4v",".ts",".mpg",".mpeg"}
        found=[]
        for item in paths:
            try:
                item=os.path.normpath(str(item))
            except Exception:
                continue
            if os.path.isdir(item):
                # Folder drop/add: recursively collect supported video files.
                try:
                    for root,dirs,files in os.walk(item):
                        for name in files:
                            fp=os.path.join(root,name)
                            if Path(fp).suffix.lower() in allowed:
                                found.append(fp)
                except Exception:
                    continue
            elif os.path.isfile(item) and Path(item).suffix.lower() in allowed:
                found.append(item)
        for f in found:
            f=os.path.normpath(f)
            if f not in self.video_compress_files:
                self.video_compress_files.append(f)
                if hasattr(self,"video_compress_list"):
                    self.video_compress_list.insert("end",f)

    def _video_compress_remove(self):
        if not hasattr(self,"video_compress_list"):
            return
        for i in reversed(self.video_compress_list.curselection()):
            try: self.video_compress_files.pop(i)
            except Exception: pass
            self.video_compress_list.delete(i)

    def _video_compress_clear(self):
        self.video_compress_files.clear()
        if hasattr(self,"video_compress_list"):
            self.video_compress_list.delete(0,"end")
        if hasattr(self,"video_compress_progress"):
            self.video_compress_progress["value"]=0
        if hasattr(self,"video_compress_percent"):
            self.video_compress_percent.config(text="0%")

    def _video_compress_start(self):
        if self.video_compress_busy:
            return
        if hasattr(self,"video_compress_list"):
            try:
                self.video_compress_files=[self.video_compress_list.get(i) for i in range(self.video_compress_list.size())]
            except Exception:
                pass
        if not self.video_compress_files:
            return messagebox.showwarning(APP_NAME,"動画を追加してください。")
        ff=tool("ffmpeg")
        if not ff:
            return messagebox.showerror(APP_NAME,self.tr("ffmpeg"))

        delete_source=bool(self.video_compress_delete_source.get())
        if delete_source:
            if not messagebox.askyesno(APP_NAME,
                "圧縮に成功した元動画を削除します。\n削除した元動画は元に戻せません。\n\n続けますか？"):
                return

        outdir=Path(self.video_compress_outdir.get().strip() or ".")
        outdir.mkdir(parents=True,exist_ok=True)
        files=list(self.video_compress_files)
        total=len(files)
        quality=self.video_compress_quality.get()
        resolution=self.video_compress_resolution.get()
        audio_br=self.video_compress_audio_bitrate.get()
        speed=self.video_compress_speed.get()
        crf_map={"高画質":"21","標準":"26","強く圧縮":"31"}
        crf=crf_map.get(quality,"26")
        preset_map={"最速":"ultrafast","高速":"veryfast","標準":"medium","高圧縮":"slow"}
        preset=preset_map.get(speed,"veryfast")
        scale_map={"1080p":"1080","720p":"720","480p":"480"}
        target_h=scale_map.get(resolution)
        video_output_map=_compression_output_map(
            files,outdir,lambda src: Path(src).stem+".mp4"
        )

        self.video_compress_busy=True
        try:
            self._cancel_work.clear(); self._user_cancelled=False; self._set_cancel_state(True)
        except Exception: pass
        self.video_compress_progress["value"]=0
        self.video_compress_percent.config(text="0%")

        def ui_progress(v):
            try:
                v=max(0.0,min(100.0,float(v)))
                self.video_compress_progress["value"]=v
                self.video_compress_percent.config(text=f"{round(v)}%")
            except Exception: pass

        def ui_finish(ok,fails,deleted,cancelled=False):
            self.video_compress_busy=False
            try:
                self._set_cancel_state(False)
                self._cancel_work.clear(); self._user_cancelled=False
            except Exception: pass
            msg=f"{ok}/{total} 件 圧縮しました。"
            if delete_source:
                msg+=f"\n元動画削除: {deleted} 件"
            if fails:
                msg+="\n\n失敗:\n"+"\n".join(fails[:8])
                messagebox.showwarning(APP_NAME,msg)
            else:
                messagebox.showinfo(APP_NAME,msg)
            try:
                self.video_compress_progress["value"]=0
                self.video_compress_percent.config(text="0%")
            except Exception: pass

        def worker():
            ok=0; fails=[]; deleted=0; cancelled=False
            for i,src in enumerate(files,1):
                if self._is_work_cancelled():
                    cancelled=True
                    break
                try:
                    dst=video_output_map[src]
                    cmd=[ff,"-y","-hide_banner","-loglevel","error","-i",src,
                         "-map","0:v:0?","-map","0:a:0?",
                         "-c:v","libx264","-preset",preset,"-crf",crf]
                    if target_h:
                        cmd += ["-vf",f"scale=-2:{target_h}:force_original_aspect_ratio=decrease"]
                    cmd += ["-c:a","aac","-b:a",audio_br,"-movflags","+faststart",dst]

                    duration=_media_duration_seconds(src)
                    def progress(frac,file_index=i):
                        overall=((file_index-1)+max(0.0,min(1.0,float(frac))))*100.0/total
                        try:self.root.after(0,ui_progress,overall)
                        except Exception:pass
                    _ffmpeg_run_progress(cmd,duration,progress)
                    if not os.path.isfile(dst) or os.path.getsize(dst)<=0:
                        raise RuntimeError("圧縮後の動画を作成できませんでした。")
                    ok+=1
                    if delete_source:
                        try:
                            os.remove(src); deleted+=1
                        except Exception as e:
                            fails.append(f"{os.path.basename(src)}: 圧縮成功 / 元動画削除失敗: {e}")
                except Exception as e:
                    if self._is_work_cancelled():
                        cancelled=True
                        break
                    fails.append(f"{os.path.basename(src)}: {e}")
                try:self.root.after(0,ui_progress,i*100.0/total)
                except Exception:pass
            try:self.root.after(0,ui_finish,ok,fails,deleted,cancelled)
            except Exception:self.video_compress_busy=False

        threading.Thread(target=worker,daemon=True).start()


    # ---------- Audio compression ----------
    def page_audio_compress(self):
        p=self.p()
        top=self.card(self.content); top.pack(fill="x",pady=(0,12))
        hdr=tk.Frame(top,bg=p["panel"]); hdr.pack(fill="x",padx=18,pady=14)
        tk.Label(hdr,text=("音声圧縮" if self.lang=="ja" else "Audio Compress"),
                 font=("Segoe UI",16,"bold"),bg=p["panel"],fg=p["text"]).pack(side="left")
        tk.Label(hdr,text=("MP3 / M4A / OGG / OPUS / FLAC" if self.lang=="ja" else "MP3 / M4A / OGG / OPUS / FLAC"),
                 font=("Segoe UI",9),bg=p["panel"],fg=p["muted"]).pack(side="left",padx=12)

        def add_audio():
            fs=filedialog.askopenfilenames(filetypes=[
                ("Audio","*.mp3 *.m4a *.aac *.adts *.wav *.flac *.ogg *.opus *.wma *.aiff *.aif"),
                ("All","*.*")])
            self._audio_compress_add(fs)
        def add_audio_folder():
            folder=filedialog.askdirectory(title=("音声フォルダを選択" if self.lang=="ja" else "Choose audio folder"))
            if folder:
                self._audio_compress_add([folder])
        for txt,cmd,primary in [
            (("+ 音声追加" if self.lang=="ja" else "+ Add Audio"),add_audio,True),
            (("+ フォルダ追加" if self.lang=="ja" else "+ Add Folder"),add_audio_folder,False),
            (("選択削除" if self.lang=="ja" else "Remove Selected"),self._audio_compress_remove,False),
            (("全消去" if self.lang=="ja" else "Clear All"),self._audio_compress_clear,False),
        ]:
            b=ctk.CTkButton(hdr,text=txt,command=cmd); self.style_button(b,primary); b.pack(side="right",padx=(8,0))

        body=self.card(self.content); body.pack(fill="both",expand=True)
        self.audio_compress_list=tk.Listbox(body,bg=p["entry"],fg=p["text"],relief="flat",bd=0,
                                            selectbackground=p["accent"],font=("Segoe UI",10))
        self.audio_compress_list.pack(fill="both",expand=True,padx=16,pady=(16,12))
        for f in self.audio_compress_files: self.audio_compress_list.insert("end",f)
        self._enable_drop(self.audio_compress_list,self._audio_compress_add)

        opts=tk.Frame(body,bg=p["panel"]); opts.pack(fill="x",padx=16,pady=(0,8))
        tk.Label(opts,text=("出力形式" if self.lang=="ja" else "Format"),bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")).pack(side="left")
        ttk.Combobox(opts,textvariable=self.audio_compress_format,state="readonly",
                     values=["MP3","M4A","OGG","OPUS","FLAC"],width=9).pack(side="left",padx=(8,16))
        tk.Label(opts,text=("ビットレート" if self.lang=="ja" else "Bitrate"),bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")).pack(side="left")
        ttk.Combobox(opts,textvariable=self.audio_compress_bitrate,state="readonly",
                     values=["64k","96k","128k","160k","192k","256k","320k"],width=8).pack(side="left",padx=(8,16))
        tk.Label(opts,text=("保存先" if self.lang=="ja" else "Output"),bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")).pack(side="left")
        tk.Entry(opts,textvariable=self.audio_compress_outdir,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",fill="x",expand=True,padx=8,ipady=7)
        b=ctk.CTkButton(opts,text=("参照" if self.lang=="ja" else "Browse"),command=lambda:self._choose_dir_var(self.audio_compress_outdir)); self.style_button(b); b.pack(side="left")

        delrow=tk.Frame(body,bg=p["panel"]); delrow.pack(fill="x",padx=16,pady=(0,8))
        ctk.CTkCheckBox(delrow,text=("圧縮成功後に元の音声を削除する" if self.lang=="ja" else "Delete source after successful compression"),
                        variable=self.audio_compress_delete_source,onvalue=True,offvalue=False).pack(side="left")

        prog=tk.Frame(body,bg=p["panel"]); prog.pack(fill="x",padx=16,pady=(4,16))
        self.audio_compress_progress=ttk.Progressbar(prog,maximum=100); self.audio_compress_progress.pack(side="left",fill="x",expand=True,padx=(0,8))
        self.audio_compress_percent=tk.Label(prog,text="0%",width=5,bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")); self.audio_compress_percent.pack(side="left",padx=(0,12))
        b=ctk.CTkButton(prog,text=("圧縮開始" if self.lang=="ja" else "Start Compress"),command=self._audio_compress_start); self.audio_compress_start_button=b; self.style_button(b,True); b.pack(side="right")
        self._add_cancel_button(prog,command=self.cancel_operation,enabled=self.audio_compress_busy)

    def _audio_compress_add(self,paths):
        allowed={".mp3",".m4a",".aac",".adts",".wav",".flac",".ogg",".opus",".wma",".aiff",".aif"}
        found=[]
        for item in paths:
            try:
                item=os.path.normpath(str(item))
            except Exception:
                continue
            if os.path.isdir(item):
                # Folder drop/add: recursively collect every supported audio file.
                try:
                    for root,dirs,files in os.walk(item):
                        for name in files:
                            fp=os.path.join(root,name)
                            if Path(fp).suffix.lower() in allowed:
                                found.append(fp)
                except Exception:
                    continue
            elif os.path.isfile(item) and Path(item).suffix.lower() in allowed:
                found.append(item)
        for f in found:
            f=os.path.normpath(f)
            if f not in self.audio_compress_files:
                self.audio_compress_files.append(f)
                if hasattr(self,"audio_compress_list"):
                    self.audio_compress_list.insert("end",f)

    def _audio_compress_remove(self):
        if not hasattr(self,"audio_compress_list"): return
        for i in reversed(self.audio_compress_list.curselection()):
            try:self.audio_compress_files.pop(i)
            except Exception:pass
            self.audio_compress_list.delete(i)

    def _audio_compress_clear(self):
        self.audio_compress_files.clear()
        if hasattr(self,"audio_compress_list"): self.audio_compress_list.delete(0,"end")
        if hasattr(self,"audio_compress_progress"): self.audio_compress_progress["value"]=0
        if hasattr(self,"audio_compress_percent"): self.audio_compress_percent.config(text="0%")

    def _audio_compress_start(self):
        if self.audio_compress_busy: return
        if hasattr(self,"audio_compress_list"):
            try:self.audio_compress_files=[self.audio_compress_list.get(i) for i in range(self.audio_compress_list.size())]
            except Exception:pass
        if not self.audio_compress_files: return messagebox.showwarning(APP_NAME,"音声を追加してください。")
        ff=tool("ffmpeg")
        if not ff: return messagebox.showerror(APP_NAME,self.tr("ffmpeg"))
        delete_source=bool(self.audio_compress_delete_source.get())
        if delete_source and not messagebox.askyesno(APP_NAME,"圧縮に成功した元音声を削除します。\n削除した元音声は元に戻せません。\n\n続けますか？"):
            return
        outdir=Path(self.audio_compress_outdir.get().strip() or "."); outdir.mkdir(parents=True,exist_ok=True)
        files=list(self.audio_compress_files); total=len(files)
        fmt=self.audio_compress_format.get().upper(); bitrate=self.audio_compress_bitrate.get()
        fmt_map={
            "MP3":(".mp3",["-c:a","libmp3lame","-b:a",bitrate]),
            "M4A":(".m4a",["-c:a","aac","-b:a",bitrate]),
            "OGG":(".ogg",["-c:a","libvorbis","-b:a",bitrate]),
            "OPUS":(".opus",["-c:a","libopus","-b:a",bitrate]),
            "FLAC":(".flac",["-c:a","flac","-compression_level","8"]),
        }
        ext,codec_args=fmt_map.get(fmt,fmt_map["MP3"])
        audio_output_map=_compression_output_map(
            files,outdir,lambda src: Path(src).stem+ext
        )
        self.audio_compress_busy=True; self.audio_compress_progress["value"]=0; self.audio_compress_percent.config(text="0%")
        try:
            self._cancel_work.clear(); self._user_cancelled=False; self._set_cancel_state(True)
        except Exception: pass
        def ui_progress(v):
            try:
                v=max(0.0,min(100.0,float(v))); self.audio_compress_progress["value"]=v; self.audio_compress_percent.config(text=f"{round(v)}%")
            except Exception:pass
        def ui_finish(ok,fails,deleted,cancelled=False):
            self.audio_compress_busy=False
            try:
                self._set_cancel_state(False)
                self._cancel_work.clear(); self._user_cancelled=False
            except Exception: pass
            msg=f"{ok}/{total} 件 圧縮しました。"
            if delete_source: msg+=f"\n元音声削除: {deleted} 件"
            if fails:
                msg+="\n\n失敗:\n"+"\n".join(fails[:8]); messagebox.showwarning(APP_NAME,msg)
            else: messagebox.showinfo(APP_NAME,msg)
            try:self.audio_compress_progress["value"]=0; self.audio_compress_percent.config(text="0%")
            except Exception:pass
        def worker():
            ok=0; fails=[]; deleted=0; cancelled=False
            for i,src in enumerate(files,1):
                if self._is_work_cancelled():
                    cancelled=True
                    break
                try:
                    dst=audio_output_map[src]
                    cmd=[ff,"-y","-hide_banner","-loglevel","error","-i",src,"-vn","-map_metadata","0"]+codec_args+[dst]
                    duration=_media_duration_seconds(src)
                    def progress(frac,file_index=i):
                        overall=((file_index-1)+max(0.0,min(1.0,float(frac))))*100.0/total
                        try:self.root.after(0,ui_progress,overall)
                        except Exception:pass
                    _ffmpeg_run_progress(cmd,duration,progress)
                    if not os.path.isfile(dst) or os.path.getsize(dst)<=0: raise RuntimeError("圧縮後の音声を作成できませんでした。")
                    ok+=1
                    if delete_source:
                        try:os.remove(src); deleted+=1
                        except Exception as e:fails.append(f"{os.path.basename(src)}: 圧縮成功 / 元音声削除失敗: {e}")
                except Exception as e:
                    if self._is_work_cancelled():
                        cancelled=True
                        break
                    fails.append(f"{os.path.basename(src)}: {e}")
                try:self.root.after(0,ui_progress,i*100.0/total)
                except Exception:pass
            try:self.root.after(0,ui_finish,ok,fails,deleted,cancelled)
            except Exception:self.audio_compress_busy=False
        threading.Thread(target=worker,daemon=True).start()

    # ---------- Image compression ----------
    def page_image_compress(self):
        p=self.p()
        top=self.card(self.content); top.pack(fill="x",pady=(0,12))
        hdr=tk.Frame(top,bg=p["panel"]); hdr.pack(fill="x",padx=18,pady=14)
        tk.Label(hdr,text=("画像圧縮" if self.lang=="ja" else "Image Compress"),font=("Segoe UI",16,"bold"),bg=p["panel"],fg=p["text"]).pack(side="left")
        tk.Label(hdr,text=("JPG / PNG / WEBP" if self.lang=="ja" else "JPG / PNG / WEBP"),font=("Segoe UI",9),bg=p["panel"],fg=p["muted"]).pack(side="left",padx=12)
        def add_images():
            fs=filedialog.askopenfilenames(filetypes=[("Images","*.jpg *.jpeg *.png *.webp *.bmp *.tif *.tiff"),("All","*.*")]); self._image_compress_add(fs)
        for txt,cmd,primary in [
            (("+ 画像追加" if self.lang=="ja" else "+ Add Images"),add_images,True),
            (("選択削除" if self.lang=="ja" else "Remove Selected"),self._image_compress_remove,False),
            (("全消去" if self.lang=="ja" else "Clear All"),self._image_compress_clear,False),
        ]:
            b=ctk.CTkButton(hdr,text=txt,command=cmd); self.style_button(b,primary); b.pack(side="right",padx=(8,0))
        body=self.card(self.content); body.pack(fill="both",expand=True)
        self.image_compress_list=tk.Listbox(body,bg=p["entry"],fg=p["text"],relief="flat",bd=0,selectbackground=p["accent"],font=("Segoe UI",10))
        self.image_compress_list.pack(fill="both",expand=True,padx=16,pady=(16,12))
        for f in self.image_compress_files:self.image_compress_list.insert("end",f)
        self._enable_drop(self.image_compress_list,self._image_compress_add)
        opts=tk.Frame(body,bg=p["panel"]); opts.pack(fill="x",padx=16,pady=(0,8))
        tk.Label(opts,text=("出力形式" if self.lang=="ja" else "Format"),bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")).pack(side="left")
        ttk.Combobox(opts,textvariable=self.image_compress_format,state="readonly",values=["元の形式","JPEG","PNG","WEBP"],width=10).pack(side="left",padx=(8,16))
        tk.Label(opts,text=("圧縮率" if self.lang=="ja" else "Compression"),bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")).pack(side="left")
        ttk.Combobox(opts,textvariable=self.image_compress_quality,state="readonly",values=["高画質","標準","強く圧縮"],width=12).pack(side="left",padx=(8,16))
        tk.Label(opts,text=("最大サイズ" if self.lang=="ja" else "Max size"),bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")).pack(side="left")
        ttk.Combobox(opts,textvariable=self.image_compress_max_size,state="readonly",values=["元のまま","3840","2560","1920","1280","800"],width=10).pack(side="left",padx=(8,16))
        tk.Label(opts,text=("保存先" if self.lang=="ja" else "Output"),bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")).pack(side="left")
        tk.Entry(opts,textvariable=self.image_compress_outdir,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",fill="x",expand=True,padx=8,ipady=7)
        b=ctk.CTkButton(opts,text=("参照" if self.lang=="ja" else "Browse"),command=lambda:self._choose_dir_var(self.image_compress_outdir)); self.style_button(b); b.pack(side="left")
        delrow=tk.Frame(body,bg=p["panel"]); delrow.pack(fill="x",padx=16,pady=(0,8))
        ctk.CTkCheckBox(delrow,text=("圧縮成功後に元の画像を削除する" if self.lang=="ja" else "Delete source after successful compression"),variable=self.image_compress_delete_source,onvalue=True,offvalue=False).pack(side="left")
        prog=tk.Frame(body,bg=p["panel"]); prog.pack(fill="x",padx=16,pady=(4,16))
        self.image_compress_progress=ttk.Progressbar(prog,maximum=100); self.image_compress_progress.pack(side="left",fill="x",expand=True,padx=(0,8))
        self.image_compress_percent=tk.Label(prog,text="0%",width=5,bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")); self.image_compress_percent.pack(side="left",padx=(0,12))
        b=ctk.CTkButton(prog,text=("圧縮開始" if self.lang=="ja" else "Start Compress"),command=self._image_compress_start); self.image_compress_start_button=b; self.style_button(b,True); b.pack(side="right")
        self._add_cancel_button(prog,command=self.cancel_operation,enabled=self.image_compress_busy)

    def _image_compress_add(self,paths):
        allowed={".jpg",".jpeg",".png",".webp",".bmp",".tif",".tiff"}
        found=[]
        for item in paths:
            try:item=os.path.normpath(str(item))
            except Exception:continue
            if os.path.isdir(item):
                # Folder drop/add: recursively collect supported image files.
                try:
                    for root,dirs,files in os.walk(item):
                        for name in files:
                            fp=os.path.join(root,name)
                            if Path(fp).suffix.lower() in allowed:
                                found.append(fp)
                except Exception:
                    continue
            elif os.path.isfile(item) and Path(item).suffix.lower() in allowed:
                found.append(item)
        for f in found:
            f=os.path.normpath(f)
            if f not in self.image_compress_files:
                self.image_compress_files.append(f)
                if hasattr(self,"image_compress_list"):self.image_compress_list.insert("end",f)

    def _image_compress_remove(self):
        if not hasattr(self,"image_compress_list"):return
        for i in reversed(self.image_compress_list.curselection()):
            try:self.image_compress_files.pop(i)
            except Exception:pass
            self.image_compress_list.delete(i)

    def _image_compress_clear(self):
        self.image_compress_files.clear()
        if hasattr(self,"image_compress_list"):self.image_compress_list.delete(0,"end")
        if hasattr(self,"image_compress_progress"):self.image_compress_progress["value"]=0
        if hasattr(self,"image_compress_percent"):self.image_compress_percent.config(text="0%")

    def _image_compress_start(self):
        if self.image_compress_busy:return
        if hasattr(self,"image_compress_list"):
            try:self.image_compress_files=[self.image_compress_list.get(i) for i in range(self.image_compress_list.size())]
            except Exception:pass
        if not self.image_compress_files:return messagebox.showwarning(APP_NAME,"画像を追加してください。")
        delete_source=bool(self.image_compress_delete_source.get())
        if delete_source and not messagebox.askyesno(APP_NAME,"圧縮に成功した元画像を削除します。\n削除した元画像は元に戻せません。\n\n続けますか？"):
            return
        outdir=Path(self.image_compress_outdir.get().strip() or "."); outdir.mkdir(parents=True,exist_ok=True)
        files=list(self.image_compress_files); total=len(files)
        outfmt=self.image_compress_format.get(); quality_name=self.image_compress_quality.get(); max_size=self.image_compress_max_size.get()
        qmap={"高画質":92,"標準":82,"強く圧縮":65}; quality=qmap.get(quality_name,82)
        try:max_px=None if max_size=="元のまま" else int(max_size)
        except Exception:max_px=None
        def _image_out_name(src):
            src_ext=Path(src).suffix.lower()
            fmt=outfmt
            if fmt=="元の形式":
                fmt={".jpg":"JPEG",".jpeg":"JPEG",".png":"PNG",".webp":"WEBP",".bmp":"PNG",".tif":"PNG",".tiff":"PNG"}.get(src_ext,"JPEG")
            ext={"JPEG":".jpg","PNG":".png","WEBP":".webp"}[fmt]
            return Path(src).stem+ext
        image_output_map=_compression_output_map(files,outdir,_image_out_name)
        self.image_compress_busy=True; self.image_compress_progress["value"]=0; self.image_compress_percent.config(text="0%")
        try:
            self._cancel_work.clear(); self._user_cancelled=False; self._set_cancel_state(True)
        except Exception: pass
        def ui_progress(v):
            try:v=max(0.0,min(100.0,float(v))); self.image_compress_progress["value"]=v; self.image_compress_percent.config(text=f"{round(v)}%")
            except Exception:pass
        def ui_finish(ok,fails,deleted,cancelled=False):
            self.image_compress_busy=False
            try:
                self._set_cancel_state(False)
                self._cancel_work.clear(); self._user_cancelled=False
            except Exception: pass
            msg=f"{ok}/{total} 件 圧縮しました。"
            if delete_source:msg+=f"\n元画像削除: {deleted} 件"
            if fails:msg+="\n\n失敗:\n"+"\n".join(fails[:8]); messagebox.showwarning(APP_NAME,msg)
            else:messagebox.showinfo(APP_NAME,msg)
            try:self.image_compress_progress["value"]=0; self.image_compress_percent.config(text="0%")
            except Exception:pass
        def worker():
            ok=0; fails=[]; deleted=0; cancelled=False
            for i,src in enumerate(files,1):
                if self._is_work_cancelled():
                    cancelled=True
                    break
                try:
                    im=Image.open(src); im.load()
                    if max_px and max(im.size)>max_px:
                        im.thumbnail((max_px,max_px),Image.Resampling.LANCZOS)
                    src_ext=Path(src).suffix.lower()
                    fmt=outfmt
                    if fmt=="元の形式":
                        fmt={".jpg":"JPEG",".jpeg":"JPEG",".png":"PNG",".webp":"WEBP",".bmp":"PNG",".tif":"PNG",".tiff":"PNG"}.get(src_ext,"JPEG")
                    ext={"JPEG":".jpg","PNG":".png","WEBP":".webp"}[fmt]
                    dst=image_output_map[src]
                    save_kwargs={}
                    if fmt=="JPEG":
                        if im.mode not in ("RGB","L"): im=im.convert("RGB")
                        save_kwargs={"quality":quality,"optimize":True,"progressive":True}
                    elif fmt=="WEBP":
                        save_kwargs={"quality":quality,"method":6}
                    elif fmt=="PNG":
                        level=6 if quality_name=="高画質" else (8 if quality_name=="標準" else 9)
                        save_kwargs={"optimize":True,"compress_level":level}
                    im.save(dst,format=fmt,**save_kwargs); im.close()
                    if not os.path.isfile(dst) or os.path.getsize(dst)<=0:raise RuntimeError("圧縮後の画像を作成できませんでした。")
                    ok+=1
                    if delete_source:
                        try:os.remove(src); deleted+=1
                        except Exception as e:fails.append(f"{os.path.basename(src)}: 圧縮成功 / 元画像削除失敗: {e}")
                except Exception as e:
                    if self._is_work_cancelled():
                        cancelled=True
                        break
                    fails.append(f"{os.path.basename(src)}: {e}")
                try:self.root.after(0,ui_progress,i*100.0/total)
                except Exception:pass
            try:self.root.after(0,ui_finish,ok,fails,deleted,cancelled)
            except Exception:self.image_compress_busy=False
        threading.Thread(target=worker,daemon=True).start()


    def page_carrozzeria_at3(self):
        p=self.p()

        top=self.card(self.content)
        top.pack(fill="x",pady=(0,12))
        hdr=tk.Frame(top,bg=p["panel"])
        hdr.pack(fill="x",padx=18,pady=14)
        tk.Label(
            hdr,
            text="カロッツェリアAT3" if self.lang=="ja" else "Carrozzeria AT3",
            font=("Segoe UI",16,"bold"),
            bg=p["panel"],fg=p["text"]
        ).pack(side="left")

        def add_at3():
            fs=filedialog.askopenfilenames(filetypes=[("Carrozzeria AT3","*.at3")])
            self._add_car_at3_paths(fs)

        def add_navirecdata():
            d=filedialog.askdirectory(title=("NAVIRECDATAフォルダを選択" if self.lang=="ja" else "Choose NAVIRECDATA folder"))
            if d:
                self._add_car_at3_paths([d])

        for text,cmd,primary in [
            (("+ NAVIRECDATA" if self.lang=="ja" else "+ NAVIRECDATA"),add_navirecdata,True),
            (("+ AT3追加" if self.lang=="ja" else "+ Add AT3"),add_at3,False),
            (("選択削除" if self.lang=="ja" else "Remove Selected"),self._remove_car_at3_selected,False),
            (("全消去" if self.lang=="ja" else "Clear All"),self._clear_car_at3,False),
        ]:
            b=ctk.CTkButton(hdr,text=text,command=cmd)
            self.style_button(b,primary)
            b.pack(side="right",padx=(8,0))

        note=self.card(self.content)
        note.pack(fill="x",pady=(0,12))
        note_text=(
            "NAVIRECDATAフォルダをそのままドラッグ＆ドロップすると、内部のAT3を再帰的に全件検出します。DATがある場合は取れるタグを自動復元します。"
            if self.lang=="ja" else
            "Drop a NAVIRECDATA folder here to recursively detect all AT3 files. When DAT metadata is available, supported tags are restored automatically."
        )
        tk.Label(note,text=note_text,wraplength=900,justify="left",
                 bg=p["panel"],fg=p["muted"],font=("Segoe UI",9)).pack(fill="x",padx=18,pady=12)

        body=self.card(self.content)
        body.pack(fill="both",expand=True)
        settings_footer=tk.Frame(body,bg=p["panel"])
        settings_footer.pack(side="bottom",fill="x")
        self.car_at3_listbox=tk.Listbox(
            body,selectmode="extended",relief="flat",bd=0,highlightthickness=0,
            font=("Segoe UI",10),bg=p["panel2"],fg=p["text"],selectbackground=p["accent"]
        )
        self.car_at3_listbox.pack(side="top",fill="both",expand=True,padx=16,pady=(16,12))
        for f in self.car_at3_files:
            self.car_at3_listbox.insert("end",f)
        self._enable_car_at3_drop(self.car_at3_listbox)

        opts=tk.Frame(settings_footer,bg=p["panel"])
        opts.pack(fill="x",padx=16,pady=(0,10))
        tk.Label(opts,text=("出力" if self.lang=="ja" else "Output"),bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")).pack(side="left")
        ttk.Combobox(opts,textvariable=self.car_at3_outfmt,state="readonly",values=["MP3","WAV","FLAC","M4A","OPUS"],width=10).pack(side="left",padx=(8,18))
        tk.Label(opts,text=("ビットレート" if self.lang=="ja" else "Bitrate"),bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")).pack(side="left")
        ttk.Combobox(opts,textvariable=self.car_at3_bitrate,state="readonly",values=["64k","96k","128k","160k","192k","256k","320k"],width=9).pack(side="left",padx=(8,12))
        tk.Label(opts,text=("サンプルレート" if self.lang=="ja" else "Sample Rate"),bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")).pack(side="left")
        ttk.Combobox(opts,textvariable=self.car_at3_sample_rate,state="readonly",
                     values=["22050","32000","44100","48000","96000"],width=9).pack(side="left",padx=(8,12))

        def _sync_opus_sample_rate(*_):
            if self.car_at3_outfmt.get()=="OPUS":
                self.car_at3_sample_rate.set("48000")
        self.car_at3_outfmt.trace_add("write",_sync_opus_sample_rate)
        _sync_opus_sample_rate()

        self.car_at3_status=tk.Label(opts,text="",bg=p["panel"],fg=p["muted"],font=("Segoe UI",9))
        self.car_at3_status.pack(side="left",padx=(8,0))

        datrow=tk.Frame(settings_footer,bg=p["panel"])
        datrow.pack(fill="x",padx=16,pady=(0,10))
        tk.Checkbutton(
            datrow,
            text=("DATからタグ自動復元" if self.lang=="ja" else "Restore tags from DAT"),
            variable=self.car_at3_restore_tags,
            bg=p["panel"],fg=p["text"],selectcolor=p["panel2"],activebackground=p["panel"],activeforeground=p["text"]
        ).pack(side="left")
        tk.Checkbutton(
            datrow,
            text=("変換成功後に元のAT3を削除" if self.lang=="ja" else "Delete source AT3 after successful conversion"),
            variable=self.car_at3_delete_source,
            bg=p["panel"],fg=p["text"],selectcolor=p["panel2"],activebackground=p["panel"],activeforeground=p["text"]
        ).pack(side="left",padx=(12,0))
        def choose_navirecdata():
            d=filedialog.askdirectory(title=("NAVIRECDATAフォルダを選択" if self.lang=="ja" else "Choose NAVIRECDATA folder"))
            if d:
                self.car_at3_navirecdata.set(d)
        bdat=ctk.CTkButton(datrow,text=("NAVIRECDATA選択" if self.lang=="ja" else "Choose NAVIRECDATA"),command=choose_navirecdata,width=145)
        self.style_button(bdat,False)
        bdat.pack(side="left",padx=(10,8))
        self.car_at3_dat_label=tk.Label(
            datrow,
            textvariable=self.car_at3_navirecdata,
            bg=p["panel"],fg=p["muted"],font=("Segoe UI",9),anchor="w"
        )
        self.car_at3_dat_label.pack(side="left",fill="x",expand=True)

        bottom=tk.Frame(settings_footer,bg=p["panel"])
        bottom.pack(fill="x",padx=16,pady=(0,16))
        self.car_at3_progress=ttk.Progressbar(bottom,maximum=100)
        self.car_at3_progress.pack(side="left",fill="x",expand=True,padx=(0,8))
        self.car_at3_percent=tk.Label(bottom,text="0%",width=5,bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold"))
        self.car_at3_percent.pack(side="left",padx=(0,12))
        b=ctk.CTkButton(bottom,text=("変換開始" if self.lang=="ja" else "Start Convert"),command=self.do_carrozzeria_at3_convert)
        self.car_at3_convert_button=b
        self.style_button(b,True)
        b.pack(side="right")
        self._add_cancel_button(bottom,command=self.cancel_operation,enabled=self.car_at3_busy)

    def _natural_path_key(self,path):
        import re
        return [int(x) if x.isdigit() else x.lower() for x in re.split(r"(\d+)", os.path.normpath(path))]

    def _find_navirecdata_in_path(self,path):
        p=os.path.abspath(path)
        if os.path.isdir(p) and os.path.basename(p).upper()=="NAVIRECDATA":
            return p
        if os.path.isdir(p):
            candidate=os.path.join(p,"NAVIRECDATA")
            if os.path.isdir(candidate):
                return candidate
        return _find_navirecdata_root(p)

    def _add_car_at3_paths(self,paths):
        # Large NAVIRECDATA folders can contain hundreds of tracks. Scan off the UI thread.
        raw_paths=[os.path.normpath(str(x)) for x in paths]
        if not raw_paths:
            return
        if hasattr(self,"car_at3_status"):
            self.car_at3_status.config(text=("検索中..." if self.lang=="ja" else "Scanning..."))

        def worker():
            rejected=[]
            discovered=[]
            navroots=[]
            for f in raw_paths:
                if os.path.isdir(f):
                    navroot=self._find_navirecdata_in_path(f)
                    scanroot=navroot or f
                    if navroot:
                        navroots.append(navroot)
                    try:
                        for root,dirs,files in os.walk(scanroot):
                            dirs.sort(key=self._natural_path_key)
                            for name in sorted(files,key=self._natural_path_key):
                                if name.lower().endswith('.at3'):
                                    discovered.append(os.path.join(root,name))
                    except Exception as e:
                        rejected.append(f"{os.path.basename(f)}: {e}")
                    continue
                if os.path.isfile(f) and os.path.splitext(f)[1].lower()=='.at3':
                    discovered.append(f)
                    root=_find_navirecdata_root(f)
                    if root:
                        navroots.append(root)
                elif os.path.exists(f):
                    rejected.append(os.path.basename(f))

            ordered=sorted(dict.fromkeys(discovered),key=self._natural_path_key)
            def apply_results():
                added=0
                existing=set(self.car_at3_files)
                for f in ordered:
                    if f not in existing:
                        self.car_at3_files.append(f)
                        existing.add(f)
                        added+=1
                        if hasattr(self,"car_at3_listbox"):
                            self.car_at3_listbox.insert("end",f)
                if navroots:
                    self.car_at3_navirecdata.set(os.path.normpath(navroots[0]))
                if hasattr(self,"car_at3_status"):
                    if added:
                        self.car_at3_status.config(text=(f"{added}曲検出" if self.lang=="ja" else f"{added} track(s) found"))
                    elif ordered:
                        self.car_at3_status.config(text=("追加済み" if self.lang=="ja" else "Already added"))
                    else:
                        self.car_at3_status.config(text=("AT3が見つかりません" if self.lang=="ja" else "No AT3 files found"))
                if rejected:
                    messagebox.showwarning(APP_NAME,("AT3またはNAVIRECDATAフォルダを追加してください。\n" if self.lang=="ja" else "Add AT3 files or a NAVIRECDATA folder.\n")+"\n".join(rejected[:8]))
            self.root.after(0,apply_results)

        threading.Thread(target=worker,daemon=True).start()

    def _add_car_at3_files(self,paths):
        # Backward-compatible alias used by older call sites.
        self._add_car_at3_paths(paths)

    def _enable_car_at3_drop(self,widget):
        if not HAS_DND:
            return False
        try:
            widget.drop_target_register(DND_FILES)
            def on_drop(e):
                try:
                    items=list(self.root.tk.splitlist(e.data))
                except Exception:
                    items=[e.data]
                paths=[]
                for p in items:
                    p=str(p).strip()
                    if p.startswith('{') and p.endswith('}'):
                        p=p[1:-1]
                    if os.path.exists(p):
                        paths.append(os.path.normpath(p))
                self._add_car_at3_paths(paths)
            widget.dnd_bind("<<Drop>>",on_drop)
            return True
        except Exception:
            return False

    def _remove_car_at3_selected(self):
        if not hasattr(self,"car_at3_listbox"):
            return
        for i in reversed(self.car_at3_listbox.curselection()):
            self.car_at3_listbox.delete(i)
            try: del self.car_at3_files[i]
            except Exception: pass

    def _clear_car_at3(self):
        self.car_at3_files.clear()
        if hasattr(self,"car_at3_listbox"):
            self.car_at3_listbox.delete(0,"end")
        if hasattr(self,"car_at3_progress"):
            self.car_at3_progress["value"]=0
        if hasattr(self,"car_at3_percent"):
            self.car_at3_percent.config(text="0%")

    def do_carrozzeria_at3_convert(self):
        if getattr(self,"car_at3_busy",False):
            return
        try:
            if hasattr(self,"car_at3_listbox"):
                self.car_at3_files=[self.car_at3_listbox.get(i) for i in range(self.car_at3_listbox.size())]
        except Exception:
            pass
        if not self.car_at3_files:
            return messagebox.showwarning(APP_NAME,"AT3ファイルを追加してください。" if self.lang=="ja" else "Add at least one AT3 file.")

        ff=tool("ffmpeg")
        if not ff:
            return messagebox.showerror(APP_NAME,self.tr("ffmpeg"))
        out=filedialog.askdirectory()
        if not out:
            return

        delete_source=bool(self.car_at3_delete_source.get())
        if delete_source:
            msg=(
                "変換に成功した元のAT3ファイルを削除します。\nこの操作は元に戻せません。続行しますか？"
                if self.lang=="ja" else
                "Successfully converted source AT3 files will be deleted.\nThis cannot be undone. Continue?"
            )
            if not messagebox.askyesno(APP_NAME,msg):
                return

        fmt=self.car_at3_outfmt.get()
        bitrate=self.car_at3_bitrate.get()
        car_sample_rate="48000" if fmt=="OPUS" else self.car_at3_sample_rate.get()
        restore_tags=bool(self.car_at3_restore_tags.get())
        nav_setting=self.car_at3_navirecdata.get().strip()
        files=list(self.car_at3_files)
        ext={"MP3":".mp3","WAV":".wav","FLAC":".flac","M4A":".m4a","OPUS":".opus"}.get(fmt,".mp3")
        total=len(files)

        self.car_at3_busy=True
        try:
            self._cancel_work.clear(); self._user_cancelled=False; self._set_cancel_state(True)
        except Exception: pass
        if hasattr(self,"car_at3_convert_button"):
            try: self.car_at3_convert_button.configure(state="disabled")
            except Exception: pass
        self.car_at3_progress["maximum"]=100
        self.car_at3_progress["value"]=0
        self.car_at3_percent.config(text="0%")
        if hasattr(self,"car_at3_status"):
            self.car_at3_status.config(text=("変換中..." if self.lang=="ja" else "Converting..."))

        def set_progress(value):
            value=max(0.0,min(100.0,float(value)))
            if hasattr(self,"car_at3_progress"):
                self.car_at3_progress["value"]=value
            if hasattr(self,"car_at3_percent"):
                self.car_at3_percent.config(text=f"{round(value)}%")

        def set_status(text):
            if hasattr(self,"car_at3_status"):
                self.car_at3_status.config(text=text)

        def worker():
            errs=[]
            deleted=[]
            succeeded=[]
            cancelled=False
            for i,src in enumerate(files,1):
                if self._is_work_cancelled():
                    cancelled=True
                    break
                full_success=False
                try:
                    if os.path.splitext(src)[1].lower() != ".at3":
                        raise ValueError("AT3以外のファイルです。")
                    stem=os.path.splitext(os.path.basename(src))[0]
                    navroot=nav_setting or _find_navirecdata_root(src)
                    target_dir=out
                    if navroot:
                        try:
                            rel_parent=os.path.relpath(os.path.dirname(src),navroot)
                            if rel_parent not in (".", os.curdir) and not rel_parent.startswith(".."):
                                target_dir=os.path.join(out,rel_parent)
                        except Exception:
                            target_dir=out
                    os.makedirs(target_dir,exist_ok=True)
                    dst=os.path.join(target_dir,stem+ext)
                    if os.path.exists(dst):
                        n=1
                        while os.path.exists(os.path.join(target_dir,f"{stem}_rescued_{n}{ext}")):
                            n+=1
                        dst=os.path.join(target_dir,f"{stem}_rescued_{n}{ext}")

                    def car_file_progress(frac, file_index=i):
                        overall=((file_index-1)+max(0.0,min(1.0,float(frac))))*100.0/total
                        self.root.after(0,set_progress,overall)
                    convert_audio(ff,src,dst,fmt,bitrate,None,car_file_progress,car_sample_rate)
                    if not os.path.isfile(dst) or os.path.getsize(dst)<=0:
                        raise RuntimeError("出力ファイルを作成できませんでした。")

                    tag_ok=True
                    if restore_tags:
                        tags, detail=read_carrozzeria_dat_tags(src, navroot)
                        if tags:
                            try:
                                write_tags(ff,dst,tags)
                                shown=tags.get("title") or os.path.basename(src)
                                self.root.after(0,set_status,(f"タグ復元: {shown}" if self.lang=="ja" else f"Tags restored: {shown}"))
                            except Exception as tag_error:
                                tag_ok=False
                                errs.append(f"{os.path.basename(src)}: タグ復元のみ失敗: {tag_error}")
                        else:
                            self.root.after(0,set_status,("DATタグなし" if self.lang=="ja" else "No DAT tags"))
                    else:
                        self.root.after(0,set_status,os.path.basename(src))

                    full_success=tag_ok
                    if full_success:
                        succeeded.append(src)
                        if delete_source:
                            try:
                                os.remove(src)
                                deleted.append(src)
                            except Exception as del_error:
                                errs.append(f"{os.path.basename(src)}: 変換成功、元ファイル削除失敗: {del_error}")
                except Exception as e:
                    if self._is_work_cancelled():
                        cancelled=True
                        break
                    errs.append(f"{os.path.basename(src)}: {e}")
                self.root.after(0,set_progress,i*100.0/total)

            def finish(cancelled=False):
                # Remove deleted sources from the visible list only after the worker is done.
                if deleted:
                    deleted_set=set(deleted)
                    self.car_at3_files=[f for f in self.car_at3_files if f not in deleted_set]
                    if hasattr(self,"car_at3_listbox"):
                        self.car_at3_listbox.delete(0,"end")
                        for f in self.car_at3_files:
                            self.car_at3_listbox.insert("end",f)
                self.car_at3_busy=False
                try:
                    self._set_cancel_state(False)
                    self._cancel_work.clear(); self._user_cancelled=False
                except Exception: pass
                if hasattr(self,"car_at3_convert_button"):
                    try: self.car_at3_convert_button.configure(state="normal")
                    except Exception: pass
                set_progress(100 if total else 0)
                converted=len(succeeded)
                msg=(
                    f"{converted}/{total} 件を変換しました。\nNAVIRECDATAのフォルダ構造を保存先にも維持しました。"
                    if self.lang=="ja" else
                    f"Converted {converted}/{total} file(s).\nNAVIRECDATA folder structure was preserved in the output."
                )
                if delete_source:
                    msg += (f"\n元のAT3を {len(deleted)} 件削除しました。" if self.lang=="ja" else f"\nDeleted {len(deleted)} source AT3 file(s).")
                if errs:
                    msg += ("\n\n注意 / 失敗:\n" if self.lang=="ja" else "\n\nWarnings / failures:\n") + "\n".join(errs[:10])
                    messagebox.showwarning(APP_NAME,msg)
                else:
                    messagebox.showinfo(APP_NAME,msg)
                set_status(("完了" if self.lang=="ja" else "Done"))
                self.root.after(700,lambda: set_progress(0))
            self.root.after(0,finish,cancelled)

        threading.Thread(target=worker,daemon=True).start()

    def _conv_percent_watch(self):
        try:
            if hasattr(self,"convpercent") and self.convpercent.winfo_exists():
                self.convpercent.config(text=f"{int(float(self.convprog.get()))}%")
                self.root.after(150,self._conv_percent_watch)
        except Exception:
            pass

    def _clear_convert_inner(self):
        if not hasattr(self,"convert_inner"):
            return
        for w in self.convert_inner.winfo_children():
            w.destroy()

    def _show_audio_convert_panel(self):
        self._clear_convert_inner()
        p=self.p()
        host=self.convert_inner

        self.files=[]
        self.listbox=tk.Listbox(
            host,
            selectmode="extended",
            bg=p["entry"],
            fg=p["text"],
            selectbackground=p["accent"],
            relief="flat",
            height=12
        )
        self.listbox.pack(fill="both",expand=True,pady=(0,8))

        controls=tk.Frame(host,bg=p["panel"])
        controls.pack(fill="x",pady=(0,8))

        def add_files():
            fs=filedialog.askopenfilenames(
                filetypes=[
                    ("Media","*.wav *.mp3 *.m4a *.aac *.flac *.ogg *.opus *.mp4 *.mkv *.webm *.mov *.avi *.m4v *.ts *.mpg *.mpeg"),
                    ("All","*.*")
                ]
            )
            for f in fs:
                if f not in self.files:
                    self.files.append(f)
                    self.listbox.insert("end",f)

        def remove_selected():
            for i in reversed(self.listbox.curselection()):
                try:self.files.pop(i)
                except Exception:pass
                self.listbox.delete(i)

        def clear_files():
            self.files.clear()
            self.listbox.delete(0,"end")

        tk.Button(controls,text="ファイル追加",command=add_files,bg=p["panel2"],fg=p["text"],relief="flat",bd=0,padx=12,pady=7).pack(side="left")
        tk.Button(controls,text="選択削除",command=remove_selected,bg=p["panel2"],fg=p["text"],relief="flat",bd=0,padx=12,pady=7).pack(side="left",padx=6)
        tk.Button(controls,text="すべて削除",command=clear_files,bg=p["panel2"],fg=p["text"],relief="flat",bd=0,padx=12,pady=7).pack(side="left")

        opts=tk.Frame(host,bg=p["panel"])
        opts.pack(fill="x",pady=6)

        tk.Label(opts,text="出力形式",bg=p["panel"],fg=p["text"]).pack(side="left")
        if not hasattr(self,"out_fmt"):
            self.outfmt=tk.StringVar(value="MP3")
        ttk.Combobox(
            opts,
            textvariable=self.outfmt,
            state="readonly",
            values=["WAV","MP3","M4A","FLAC","AAC","ADTS","OGG","OPUS","MP4 (H.264/AAC)","MKV","WEBM","MOV"],
            width=20
        ).pack(side="left",padx=8)

        tk.Label(opts,text="音質",bg=p["panel"],fg=p["text"]).pack(side="left",padx=(8,0))
        if not hasattr(self,"bitrate"):
            self.bitrate=tk.StringVar(value="320k")
        ttk.Combobox(opts,textvariable=self.bitrate,state="readonly",
                     values=["64k","96k","128k","160k","192k","256k","320k"],width=8).pack(side="left",padx=6)

        delete_opts=tk.Frame(host,bg=p["panel"])
        delete_opts.pack(fill="x",pady=(4,6))
        ctk.CTkCheckBox(
            delete_opts,
            text="変換成功後に元のファイルを削除する",
            variable=self.delete_source_after_convert,
            onvalue=True,
            offvalue=False
        ).pack(side="left")

        tk.Button(
            opts,
            text="▶ 変換開始",
            command=self.do_convert,
            bg=p["accent"],
            fg="white",
            activebackground=p["accent2"],
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=18,
            pady=9
        ).pack(side="left",padx=8)

        progrow=tk.Frame(host,bg=p["panel"])
        progrow.pack(fill="x",pady=(10,2))
        if not hasattr(self,"convprog"):
            self.convprog=tk.DoubleVar(value=0)
        ttk.Progressbar(progrow,variable=self.convprog,maximum=100).pack(side="left",fill="x",expand=True)
        self.convpercent=tk.Label(progrow,text="0%",width=6,bg=p["panel"],fg=p["text"])
        self.convpercent.pack(side="left",padx=(8,0))
        self._conv_percent_watch()

        # Re-enable drag & drop on the rebuilt list.
        try:
            if DND_FILES:
                self.listbox.drop_target_register(DND_FILES)
                self.listbox.dnd_bind("<<Drop>>",lambda e:self._drop_convert_files(e))
        except Exception:
            pass

    def _show_universal_convert_panel(self):
        self._clear_convert_inner()
        p=self.p()
        host=self.convert_inner

        tk.Label(
            host,
            text="拡張子・形式変換",
            font=("Segoe UI",14,"bold"),
            bg=p["panel"],
            fg=p["text"]
        ).pack(anchor="w",pady=(0,8))

        self.uc_files=[]
        self.uc_list=tk.Listbox(
            host,
            selectmode="extended",
            bg=p["entry"],
            fg=p["text"],
            selectbackground=p["accent"],
            relief="flat",
            height=11
        )
        self.uc_list.pack(fill="both",expand=True,pady=(0,8))

        r=tk.Frame(host,bg=p["panel"])
        r.pack(fill="x",pady=(0,8))

        def add_uc():
            fs=filedialog.askopenfilenames(filetypes=[("All","*.*")])
            for f in fs:
                self.uc_files.append(f)
                self.uc_list.insert("end",f)

        def remove_uc():
            for i in reversed(self.uc_list.curselection()):
                try:self.uc_files.pop(i)
                except Exception:pass
                self.uc_list.delete(i)

        tk.Button(r,text="ファイル追加",command=add_uc,bg=p["panel2"],fg=p["text"],relief="flat",bd=0,padx=12,pady=7).pack(side="left")
        tk.Button(r,text="選択削除",command=remove_uc,bg=p["panel2"],fg=p["text"],relief="flat",bd=0,padx=12,pady=7).pack(side="left",padx=6)
        tk.Button(r,text="すべて削除",command=lambda:(self.uc_files.clear(),self.uc_list.delete(0,"end")),bg=p["panel2"],fg=p["text"],relief="flat",bd=0,padx=12,pady=7).pack(side="left")

        outrow=tk.Frame(host,bg=p["panel"])
        outrow.pack(fill="x",pady=6)

        tk.Label(outrow,text="変換先",bg=p["panel"],fg=p["text"]).pack(side="left")
        if not hasattr(self,"uc_format"):
            self.uc_format=tk.StringVar(value="MP3")
        ttk.Combobox(
            outrow,
            textvariable=self.uc_format,
            state="readonly",
            values=[
                "MP4","MKV","WEBM","MOV","AVI",
                "MP3","WAV","FLAC","M4A","AAC","OGG","OPUS",
                "PNG","JPEG","WEBP","BMP","TIFF","GIF","ICO"
            ],
            width=16
        ).pack(side="left",padx=8)

        # Reuse existing universal conversion worker if available.
        run_cmd=None
        for candidate in ("_universal_run","universal_run","run_universal"):
            if hasattr(self,candidate):
                run_cmd=getattr(self,candidate)
                break

        if run_cmd:
            tk.Button(
                outrow,
                text="一括変換",
                command=run_cmd,
                bg=p["accent"],
                fg="white",
                relief="flat",
                bd=0,
                padx=16,
                pady=8
            ).pack(side="left",padx=8)
        else:
            tk.Label(outrow,text="既存の変換処理が見つかりません",bg=p["panel"],fg="#ff7777").pack(side="left",padx=8)

        try:
            if DND_FILES:
                self.uc_list.drop_target_register(DND_FILES)
                self.uc_list.dnd_bind("<<Drop>>",self._uc_drop)
        except Exception:
            pass

    def add_files(self):
        fs=filedialog.askopenfilenames(filetypes=[("Audio / Video","*.mp3 *.m4a *.wav *.aac *.adts *.flac *.mp4 *.mkv *.webm *.mov *.m4v *.avi *.ts *.mpg *.mpeg"),("All","*.*")])
        for f in fs:
            if f not in self.files:self.files.append(f)
        if hasattr(self,"listbox"):
            self.listbox.delete(0,"end")
            for f in self.files:self.listbox.insert("end",f)

    def add_convert_folder(self):
        folder=filedialog.askdirectory(title=("変換する音声・動画フォルダーを選択" if self.lang=="ja" else "Choose audio/video folder"))
        if not folder:
            return
        allowed={".mp3",".m4a",".wav",".aac",".adts",".flac",".ogg",".opus", ".at3", ".mp4",".mkv",".webm",".mov",".m4v",".avi",".ts",".mpg",".mpeg"}
        existing=set(self.files)
        count=0
        for base, dirs, names in os.walk(folder):
            dirs.sort()
            for name in sorted(names):
                if os.path.splitext(name)[1].lower() not in allowed:
                    continue
                path=os.path.join(base,name)
                if path not in existing:
                    self.files.append(path)
                    existing.add(path)
                    count+=1
        if hasattr(self,"listbox"):
            self.listbox.delete(0,"end")
            for path in self.files:
                self.listbox.insert("end",path)
        if not count:
            messagebox.showinfo(APP_NAME,"新しく追加できる対応ファイルがありません。")

    def remove_selected(self):
        if not hasattr(self,"listbox"): return
        sel=list(self.listbox.curselection())
        for i in reversed(sel):
            self.listbox.delete(i)
            del self.files[i]

    def clear_files(self):
        self.files.clear()
        if hasattr(self,"listbox"):
            self.listbox.delete(0,"end")

    def do_convert(self):
        # Long FFmpeg jobs run in a worker so the v31.77 UI stays responsive.
        if getattr(self, "_convert_running", False):
            return
        try:
            if hasattr(self,"listbox"):
                self.files=[self.listbox.get(i) for i in range(self.listbox.size())]
        except Exception:
            pass

        if not self.files:
            return messagebox.showwarning(APP_NAME,self.tr("need_files"))

        delete_originals=bool(self.delete_source_after_convert.get())
        if delete_originals:
            if not messagebox.askyesno(
                APP_NAME,
                "変換に成功した元ファイルを削除します。\n"
                "削除した元ファイルは元に戻せません。\n\n"
                "続けますか？"
            ):
                return

        ff=tool("ffmpeg")
        if not ff:
            return messagebox.showerror(APP_NAME,self.tr("ffmpeg"))

        out=filedialog.askdirectory()
        if not out:
            return

        fmt=self.outfmt.get()
        extmap={
            "WAV":".wav", "MP3":".mp3", "M4A":".m4a", "OPUS":".opus", "FLAC":".flac",
            "ADTS (.adts)":".adts", "MP4 (H.264/AAC)":".mp4",
            "MKV (H.264/AAC)":".mkv", "WEBM (VP9/Opus)":".webm",
            "MOV (H.264/AAC)":".mov"
        }
        if fmt not in extmap:
            return messagebox.showerror(APP_NAME,"出力形式を選び直してください。")

        files=list(self.files)
        ext=extmap[fmt]
        bitrate=self.bitrate.get()
        sample_rate=None
        total=len(files)
        self._convert_running=True
        try:
            self._cancel_work.clear(); self._user_cancelled=False; self._set_cancel_state(True)
        except Exception: pass
        self.convprog["maximum"]=100
        self.convprog["value"]=0
        self.convpercent.config(text="0%")
        self.root.update_idletasks()

        def ui_progress(percent):
            try:
                percent=max(0.0,min(100.0,float(percent)))
                self.convprog["value"]=percent
                self.convpercent.config(text=f"{round(percent)}%")
            except Exception:
                pass

        def ui_finish(errs, delete_errs, deleted_count, cancelled=False):
            self._convert_running=False
            try:
                self._set_cancel_state(False)
                self._cancel_work.clear(); self._user_cancelled=False
            except Exception: pass
            converted_count=total-len(errs)
            result_msg=f"{converted_count}/{total} 件 変換しました。"
            if delete_originals:
                result_msg += f"\n元ファイル削除: {deleted_count} 件"
            if errs:
                result_msg += "\n\n変換失敗:\n" + "\n".join(errs[:8])
            if delete_errs:
                result_msg += "\n\n元ファイル削除失敗:\n" + "\n".join(delete_errs[:8])

            if cancelled:
                result_msg += ("\n\nキャンセルしました。" if self.lang=="ja" else "\n\nCancelled.")
                messagebox.showinfo(APP_NAME,result_msg)
            elif errs or delete_errs:
                messagebox.showwarning(APP_NAME,result_msg)
            else:
                messagebox.showinfo(APP_NAME,result_msg)

            try:
                self.files.clear()
                if hasattr(self,"listbox"):
                    self.listbox.delete(0,"end")
                self.convprog["value"]=0
                self.convpercent.config(text="0%")
            except Exception:
                pass

        # Maintain the original folder hierarchy for batch conversions.
        # For files under NAVIRECDATA, e.g. OPL001/OPL001/TRACK01.AT3,
        # the destination becomes OPL001/OPL001/TRACK01.opus.
        input_parents=[os.path.normcase(os.path.abspath(os.path.dirname(p))) for p in files]
        try:
            common_input_root=os.path.commonpath(input_parents)
        except ValueError:  # Different Windows drives
            common_input_root=None
        separate_folders=len(set(input_parents))>1
        def destination_directory(src):
            parent=os.path.normcase(os.path.abspath(os.path.dirname(src)))
            if not separate_folders:
                return out
            if common_input_root:
                relative=os.path.relpath(parent, common_input_root)
                if relative not in (".", ""):
                    return os.path.join(out,relative)
                return os.path.join(out, "_root")
            # Different drives cannot have a shared relative parent.
            drive,rest=os.path.splitdrive(parent)
            drive_label=_sanitize_output_folder_name(drive.replace(":", "") or "root")
            return os.path.join(out, drive_label, rest.lstrip("/\\"))

        def worker():
            errs=[]
            delete_errs=[]
            deleted_count=0
            cancelled=False
            used_destinations=set()
            for i,src in enumerate(files,1):
                if self._is_work_cancelled():
                    cancelled=True
                    break
                try:
                    target_dir=destination_directory(src)
                    os.makedirs(target_dir,exist_ok=True)
                    dst=os.path.join(target_dir,os.path.splitext(os.path.basename(src))[0]+ext)
                    if os.path.normcase(os.path.abspath(src)) == os.path.normcase(os.path.abspath(dst)):
                        stem=os.path.splitext(os.path.basename(src))[0]
                        dst=os.path.join(out,stem+"_converted"+ext)
                    # Files from different subfolders may share names (TRACK01 etc.).
                    # Never overwrite another conversion or an existing output.
                    proposed=dst
                    stem,extension=os.path.splitext(proposed)
                    serial=2
                    while os.path.normcase(os.path.abspath(dst)) in used_destinations or os.path.exists(dst):
                        dst=f"{stem}_{serial}{extension}"
                        serial+=1
                    used_destinations.add(os.path.normcase(os.path.abspath(dst)))
                    def file_progress(frac, file_index=i):
                        overall=((file_index-1)+max(0.0,min(1.0,float(frac))))*100.0/total
                        try:
                            self.root.after(0,ui_progress,overall)
                        except Exception:
                            pass
                    convert_audio(ff,src,dst,fmt,bitrate,None,file_progress,sample_rate)
                    if delete_originals:
                        if os.path.isfile(dst) and os.path.getsize(dst)>0:
                            try:
                                os.remove(src)
                                deleted_count += 1
                            except Exception as de:
                                delete_errs.append(f"{os.path.basename(src)}: {de}")
                        else:
                            delete_errs.append(f"{os.path.basename(src)}: 出力ファイルを確認できないため元ファイルは削除しませんでした。")
                except Exception as e:
                    errs.append(f"{os.path.basename(src)}: {e}")
                try:
                    self.root.after(0,ui_progress,i*100.0/total)
                except Exception:
                    pass
            try:
                self.root.after(0,ui_finish,errs,delete_errs,deleted_count,cancelled)
            except Exception:
                self._convert_running=False

        threading.Thread(target=worker,daemon=True).start()


    def _parse_drop_files(self,data):
        """Parse Tcl/Tk drag-and-drop file list safely."""
        try:
            items=list(self.root.tk.splitlist(data))
        except Exception:
            items=[data]
        out=[]
        for p in items:
            p=str(p).strip()
            if p.startswith("{") and p.endswith("}"):
                p=p[1:-1]
            # Accept both files and folders. Compression pages expand folders recursively.
            if os.path.isfile(p) or os.path.isdir(p):
                out.append(os.path.normpath(p))
        return out

    def _enable_drop(self,widget,callback):
        if not HAS_DND:
            return False
        try:
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind("<<Drop>>",lambda e: callback(self._parse_drop_files(e.data)))
            return True
        except Exception:
            return False

    def _add_convert_dropped(self,paths):
        allowed={".mp3",".m4a",".wav",".aac",".adts",".flac",
                 ".mp4",".mkv",".webm",".mov",".m4v",".avi",".ts",".mpg",".mpeg"}
        paths=[p for p in paths if os.path.splitext(p)[1].lower() in allowed]
        for p in paths:
            if p not in self.files:
                self.files.append(p)
                if hasattr(self,"listbox"):
                    self.listbox.insert("end",p)


    def _add_batch_dropped(self,paths):
        if not hasattr(self,"batch_files"):
            self.batch_files=[]
        for p in paths:
            if p not in self.batch_files:
                self.batch_files.append(p)
        if hasattr(self,"batch_listbox"):
            self.batch_listbox.delete(0,"end")
            for p in self.batch_files:
                self.batch_listbox.insert("end",p)



    # ---------- Image editor ----------
    def page_imageedit(self):
        p=self.p(); c=self.card(self.content); c.pack(fill="both",expand=True)
        tk.Label(c,text="画像編集",font=("Segoe UI",18,"bold"),bg=p["panel"],fg=p["text"]).pack(anchor="w",padx=20,pady=(18,10))
        tk.Label(c,text="回転・反転・明るさ・コントラスト・彩度・リサイズ・文字入れ・形式変換",
                 bg=p["panel"],fg=p["muted"]).pack(anchor="w",padx=20,pady=(0,12))

        self.img_input=tk.StringVar()
        self.img_output=tk.StringVar()
        self.img_width=tk.StringVar()
        self.img_height=tk.StringVar()
        self.img_brightness=tk.DoubleVar(value=1.0)
        self.img_contrast=tk.DoubleVar(value=1.0)
        self.img_color=tk.DoubleVar(value=1.0)
        self.img_rotate=tk.StringVar(value="0°")
        self.img_flip=tk.StringVar(value="なし")
        self.img_text=tk.StringVar()
        self.img_font=tk.StringVar(value="Arial")
        self.img_font_file=tk.StringVar()
        self.img_fontsize=tk.StringVar(value="36")
        self.img_preview_photo=None
        self.img_text_x=tk.StringVar(value="20")
        self.img_text_y=tk.StringVar(value="20")
        self.img_format=tk.StringVar(value="PNG")

        def filerow(title,var,save=False):
            r=tk.Frame(c,bg=p["panel"]);r.pack(fill="x",padx=20,pady=5)
            tk.Label(r,text=title,width=10,anchor="w",bg=p["panel"],fg=p["text"]).pack(side="left")
            tk.Entry(r,textvariable=var,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",fill="x",expand=True,ipady=8,padx=(0,8))
            def choose():
                if save:
                    ext="."+self.img_format.get().lower().replace("jpeg","jpg")
                    f=filedialog.asksaveasfilename(defaultextension=ext,filetypes=[("Image","*.png *.jpg *.jpeg *.webp *.bmp *.gif *.tif *.tiff *.ico")])
                else:
                    f=filedialog.askopenfilename(filetypes=[("Image","*.png *.jpg *.jpeg *.webp *.bmp *.gif *.tif *.tiff *.ico *.ppm *.pgm"),("All","*.*")])
                if f:
                    var.set(f)
                    if not save:
                        try: self.root.after(100, self._image_preview_update)
                        except Exception: pass
            b=ctk.CTkButton(r,text="参照",command=choose);self.style_button(b);b.pack(side="left")
        filerow("入力",self.img_input)
        filerow("出力",self.img_output,True)

        r=tk.Frame(c,bg=p["panel"]);r.pack(fill="x",padx=20,pady=6)
        tk.Label(r,text="形式",bg=p["panel"],fg=p["text"]).pack(side="left")
        ttk.Combobox(r,textvariable=self.img_format,state="readonly",values=["PNG","JPEG","WEBP","BMP","TIFF","ICO"],width=10).pack(side="left",padx=8)
        tk.Label(r,text="サイズ",bg=p["panel"],fg=p["text"]).pack(side="left",padx=(15,0))
        tk.Entry(r,textvariable=self.img_width,width=7,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",ipady=6,padx=(8,2))
        tk.Label(r,text="×",bg=p["panel"],fg=p["text"]).pack(side="left")
        tk.Entry(r,textvariable=self.img_height,width=7,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",ipady=6,padx=(2,8))
        tk.Label(r,text="空欄=元サイズ",bg=p["panel"],fg=p["muted"]).pack(side="left")

        r=tk.Frame(c,bg=p["panel"]);r.pack(fill="x",padx=20,pady=6)
        tk.Label(r,text="回転",bg=p["panel"],fg=p["text"]).pack(side="left")
        ttk.Combobox(r,textvariable=self.img_rotate,state="readonly",values=["0°","90°","180°","270°"],width=8).pack(side="left",padx=8)
        tk.Label(r,text="反転",bg=p["panel"],fg=p["text"]).pack(side="left",padx=(12,0))
        ttk.Combobox(r,textvariable=self.img_flip,state="readonly",values=["なし","左右","上下"],width=8).pack(side="left",padx=8)

        # sliders
        for title,var in [("明るさ",self.img_brightness),("コントラスト",self.img_contrast),("彩度",self.img_color)]:
            r=tk.Frame(c,bg=p["panel"]);r.pack(fill="x",padx=20,pady=3)
            tk.Label(r,text=title,width=10,anchor="w",bg=p["panel"],fg=p["text"]).pack(side="left")
            tk.Scale(r,from_=0.2,to=2.0,resolution=0.05,orient="horizontal",variable=var,
                     bg=p["panel"],fg=p["text"],highlightthickness=0,troughcolor=p["panel2"],
                     activebackground=p["accent"]).pack(side="left",fill="x",expand=True)

        textcard=self.card(c);textcard.pack(fill="x",padx=20,pady=10)
        tk.Label(textcard,text="文字入れ",font=("Segoe UI",11,"bold"),bg=p["panel"],fg=p["text"]).pack(anchor="w",padx=14,pady=(12,6))
        r=tk.Frame(textcard,bg=p["panel"]);r.pack(fill="x",padx=14,pady=5)
        tk.Entry(r,textvariable=self.img_text,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",fill="x",expand=True,ipady=7)
        tk.Label(r,text="サイズ",bg=p["panel"],fg=p["text"]).pack(side="left",padx=(10,4))
        tk.Entry(r,textvariable=self.img_fontsize,width=6,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",ipady=7)
        r2=tk.Frame(textcard,bg=p["panel"]);r2.pack(fill="x",padx=14,pady=(4,12))
        tk.Label(r2,text="フォント",bg=p["panel"],fg=p["text"]).pack(side="left")
        self.img_font_box=ttk.Combobox(r2,textvariable=self.img_font,state="readonly",width=34)
        self.img_font_box.pack(side="left",padx=8)
        try:
            import tkinter.font as tkfont
            fonts=sorted(set(tkfont.families(self.root)))
            self.img_font_box["values"]=fonts
            if "Arial" not in fonts and fonts: self.img_font.set(fonts[0])
        except Exception: self.img_font_box["values"]=["Arial"]
        def choose_font_file():
            f=filedialog.askopenfilename(filetypes=[("Font","*.ttf *.otf *.ttc"),("All","*.*")])
            if f:
                self.img_font_file.set(f)
                self._image_preview_update()
        fb=tk.Button(r2,text="フォント追加",command=choose_font_file,bg=p["panel2"],fg=p["text"],relief="flat",bd=0)
        fb.pack(side="left",padx=(0,8))
        tk.Label(r2,text="X",bg=p["panel"],fg=p["text"]).pack(side="left")
        tk.Entry(r2,textvariable=self.img_text_x,width=6,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",ipady=6,padx=4)
        tk.Label(r2,text="Y",bg=p["panel"],fg=p["text"]).pack(side="left")
        tk.Entry(r2,textvariable=self.img_text_y,width=6,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",ipady=6,padx=4)

        buttons=tk.Frame(c,bg=p["panel"]);buttons.pack(anchor="w",padx=20,pady=(8,8))
        pb=tk.Button(buttons,text="プレビュー",command=self._image_preview_update,bg=p["panel2"],fg=p["text"],relief="flat",bd=0,padx=12,pady=7)
        pb.pack(side="left",padx=(0,6))
        b=tk.Button(buttons,text="画像を書き出す",command=self._imageedit_run,bg=p["accent"],fg="white",relief="flat",bd=0,padx=12,pady=7)
        b.pack(side="left")
        prev_box=self.card(c); prev_box.pack(fill="both",expand=True,padx=20,pady=(0,14))
        tk.Label(prev_box,text="▼ プレビュー画面（下に表示）",font=("Segoe UI",11,"bold"),
                 bg=p["panel"],fg=p["accent2"]).pack(anchor="w",padx=12,pady=(10,4))
        self.img_preview=tk.Label(prev_box,text="画像を選んで「プレビュー」を押すとここに表示されます",
                                  bg=p["panel2"],fg=p["muted"],height=14)
        self.img_preview.pack(fill="both",expand=True,padx=12,pady=(0,12))

    def _image_preview_update(self):
        if not hasattr(self,"img_preview"): return
        inp=self.img_input.get().strip()
        if not inp: return messagebox.showwarning(APP_NAME,"入力画像を選んでください。")
        try:
            from PIL import ImageTk
            im=self._imageedit_make_image()
            im.thumbnail((760,300),Image.Resampling.LANCZOS)
            self.img_preview_photo=ImageTk.PhotoImage(im)
            self.img_preview.configure(image=self.img_preview_photo,text="")
        except Exception as e:
            self.img_preview.configure(image="",text="プレビュー失敗: "+str(e))

    def _list_system_fonts(self):
        """Return readable font family/file labels available on Windows and macOS."""
        names=[
            "Arial","Arial Black","Calibri","Cambria","Candara","Comic Sans MS","Consolas",
            "Constantia","Corbel","Courier New","Georgia","Impact","Lucida Console","Lucida Sans Unicode",
            "Microsoft Sans Serif","Palatino Linotype","Segoe UI","Segoe UI Bold","Tahoma","Times New Roman",
            "Trebuchet MS","Verdana","Yu Gothic","Yu Gothic UI","Meiryo","Meiryo UI","MS Gothic","MS Mincho",
            "MS PGothic","MS PMincho","Yu Mincho","BIZ UDGothic","BIZ UDMincho","UD Digi Kyokasho N-R",
            "Helvetica","Helvetica Neue","SF Pro","Hiragino Sans","Hiragino Mincho ProN","Osaka",
        ]
        font_dirs=[]
        if os.name=="nt":
            font_dirs=[Path(os.environ.get("WINDIR",r"C:\\Windows"))/"Fonts"]
        elif sys.platform=="darwin":
            font_dirs=[Path("/System/Library/Fonts"),Path("/Library/Fonts"),Path.home()/"Library/Fonts"]
        for fonts_dir in font_dirs:
            try:
                for f in sorted(fonts_dir.rglob("*")):
                    if f.is_file() and f.suffix.lower() in (".ttf",".ttc",".otf"):
                        label=f.stem
                        if label not in names:
                            names.append(label)
            except Exception:
                pass
        seen=set(); out=[]
        for n in names:
            if n not in seen:
                seen.add(n); out.append(n)
        return out

    def _find_system_font_file(self,family):
        font_dirs=[]
        if os.name=="nt":
            font_dirs=[Path(os.environ.get("WINDIR",r"C:\\Windows"))/"Fonts"]
        elif sys.platform=="darwin":
            font_dirs=[Path.home()/"Library/Fonts",Path("/Library/Fonts"),Path("/System/Library/Fonts")]
        else:
            return None
        key=re.sub(r"[^a-z0-9]","",str(family).lower())
        exact=[]; fuzzy=[]
        for fonts_dir in font_dirs:
            try:
                for f in fonts_dir.rglob("*"):
                    if not f.is_file() or f.suffix.lower() not in (".ttf",".ttc",".otf"):
                        continue
                    stem=f.stem
                    if stem.lower()==str(family).lower(): exact.append(f)
                    norm=re.sub(r"[^a-z0-9]","",stem.lower())
                    if key and (key in norm or norm in key): fuzzy.append(f)
            except Exception:
                pass
        hit=(exact or fuzzy)
        return str(hit[0]) if hit else None

    def _imageedit_make_image(self):
        inp=self.img_input.get().strip()
        if not inp: raise ValueError("入力画像を選んでください。")
        im=Image.open(inp).convert("RGBA")
        rot={"0°":0,"90°":-90,"180°":180,"270°":-270}[self.img_rotate.get()]
        if rot: im=im.rotate(rot,expand=True)
        if self.img_flip.get()=="左右": im=ImageOps.mirror(im)
        elif self.img_flip.get()=="上下": im=ImageOps.flip(im)
        im=ImageEnhance.Brightness(im).enhance(float(self.img_brightness.get()))
        im=ImageEnhance.Contrast(im).enhance(float(self.img_contrast.get()))
        im=ImageEnhance.Color(im).enhance(float(self.img_color.get()))
        w=self.img_width.get().strip();h=self.img_height.get().strip()
        if w or h:
            ow,oh=im.size
            nw=int(w) if w else max(1,round(ow*(int(h)/oh)))
            nh=int(h) if h else max(1,round(oh*(int(w)/ow)))
            im=im.resize((nw,nh),Image.Resampling.LANCZOS)
        txt=self.img_text.get()
        if txt:
            draw=ImageDraw.Draw(im);size=max(6,int(self.img_fontsize.get() or 36))
            fp=self.img_font_file.get().strip() or self._find_system_font_file(self.img_font.get())
            try:font=ImageFont.truetype(fp,size) if fp else ImageFont.load_default()
            except Exception:font=ImageFont.load_default()
            draw.text((int(self.img_text_x.get() or 20),int(self.img_text_y.get() or 20)),txt,font=font,fill="white",stroke_width=2,stroke_fill="black")
        return im

    def _imageedit_run(self):
        inp=self.img_input.get().strip()
        if not inp:return messagebox.showwarning(APP_NAME,"入力画像を選んでください。")
        fmt=self.img_format.get();ext={"PNG":".png","JPEG":".jpg","WEBP":".webp","BMP":".bmp","TIFF":".tiff","ICO":".ico"}[fmt]
        out=self.img_output.get().strip() or str(Path(inp).with_name(Path(inp).stem+"_edited"+ext))
        try:
            im=self._imageedit_make_image()
            if fmt=="JPEG":im.convert("RGB").save(out,"JPEG",quality=95)
            elif fmt=="ICO":im.save(out,"ICO",sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
            else:im.save(out,fmt)
            messagebox.showinfo(APP_NAME,f"画像を書き出しました。\n{out}")
        except Exception as e:messagebox.showerror(APP_NAME,f"画像編集エラー:\\n{e}")

    # ---------- Universal extension converter ----------
    def page_universal(self):
        p=self.p(); c=self.card(self.content);c.pack(fill="both",expand=True)
        tk.Label(c,text="画像変換",font=("Segoe UI",18,"bold"),bg=p["panel"],fg=p["text"]).pack(anchor="w",padx=20,pady=(18,10))
        tk.Label(c,text="画像ファイルだけを別の画像形式に変換します（PNG / JPEG / WEBP / BMP / TIFF / GIF / ICO）",
                 bg=p["panel"],fg=p["muted"]).pack(anchor="w",padx=20,pady=(0,12))
        self.uni_files=[]
        self.uni_outdir=tk.StringVar(value=os.path.join(os.path.expanduser("~"),"Pictures","Converted"))
        self.uni_fmt=tk.StringVar(value="PNG")

        r=tk.Frame(c,bg=p["panel"]);r.pack(fill="x",padx=20,pady=6)
        b=ctk.CTkButton(r,text="ファイル追加",command=self._universal_add);self.style_button(b,True);b.pack(side="left")
        b=ctk.CTkButton(r,text="選択削除",command=self._universal_remove);self.style_button(b);b.pack(side="left",padx=8)
        b=ctk.CTkButton(r,text="すべてクリア",command=self._universal_clear);self.style_button(b);b.pack(side="left")

        self.uni_list=tk.Listbox(c,selectmode="extended",relief="flat",bd=0,highlightthickness=0,
                                bg=p["panel2"],fg=p["text"],selectbackground=p["accent"])
        self.uni_list.pack(fill="both",expand=True,padx=20,pady=10)
        self._enable_drop(self.uni_list,self._universal_drop)

        r=tk.Frame(c,bg=p["panel"]);r.pack(fill="x",padx=20,pady=6)
        tk.Label(r,text="出力形式",bg=p["panel"],fg=p["text"]).pack(side="left")
        ttk.Combobox(r,textvariable=self.uni_fmt,state="readonly",width=22,
                     values=["PNG","JPEG","WEBP","BMP","TIFF","GIF","ICO"]).pack(side="left",padx=8)
        tk.Label(r,text="保存先",bg=p["panel"],fg=p["text"]).pack(side="left",padx=(15,0))
        tk.Entry(r,textvariable=self.uni_outdir,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",fill="x",expand=True,padx=8,ipady=7)
        b=ctk.CTkButton(r,text="参照",command=lambda:self._choose_dir_var(self.uni_outdir));self.style_button(b);b.pack(side="left")

        delete_row=tk.Frame(c,bg=p["panel"])
        delete_row.pack(fill="x",padx=20,pady=(8,0))
        ctk.CTkCheckBox(
            delete_row,
            text="変換成功後に元のファイルを削除する",
            variable=self.delete_source_after_convert,
            onvalue=True,
            offvalue=False
        ).pack(side="left")
        tk.Label(
            delete_row,
            text="※ 変換に失敗した元ファイルは削除しません。",
            bg=p["panel"],
            fg=p["muted"],
            font=("Segoe UI",9)
        ).pack(side="left",padx=(10,0))

        uni_progress_row=tk.Frame(c,bg=p["panel"])
        uni_progress_row.pack(fill="x",padx=20,pady=(10,0))
        self.uni_progress=ttk.Progressbar(uni_progress_row,maximum=100)
        self.uni_progress.pack(side="left",fill="x",expand=True,padx=(0,8))
        self.uni_percent=tk.Label(uni_progress_row,text="0%",width=5,bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold"))
        self.uni_percent.pack(side="left")

        b=ctk.CTkButton(c,text="変換開始",command=self._universal_start);self.style_button(b,True);b.pack(anchor="e",padx=20,pady=(10,18))

    def _choose_dir_var(self,var):
        d=filedialog.askdirectory()
        if d:var.set(d)

    def _universal_add(self):
        fs=filedialog.askopenfilenames(filetypes=[
            ("Image","*.png *.jpg *.jpeg *.webp *.bmp *.gif *.tif *.tiff *.ico *.ppm *.pgm"),
            ("All","*.*"),
        ])
        self._universal_add_files(fs)

    def _universal_drop(self,files):
        self._universal_add_files(files)

    def _universal_add_files(self,fs):
        img_ext={".png",".jpg",".jpeg",".webp",".bmp",".gif",".tif",".tiff",".ico",".ppm",".pgm"}
        for f in fs:
            if os.path.isfile(f) and f not in self.uni_files and Path(f).suffix.lower() in img_ext:
                self.uni_files.append(f);self.uni_list.insert("end",f)

    def _universal_remove(self):
        for i in reversed(self.uni_list.curselection()):
            self.uni_files.pop(i);self.uni_list.delete(i)

    def _universal_clear(self):
        self.uni_files.clear();self.uni_list.delete(0,"end")
        if hasattr(self,"uni_progress"):
            self.uni_progress["value"]=0
        if hasattr(self,"uni_percent"):
            self.uni_percent.config(text="0%")

    def _universal_start(self):
        if not self.uni_files:return messagebox.showwarning(APP_NAME,"ファイルを追加してください。")
        delete_originals=bool(self.delete_source_after_convert.get())
        if delete_originals:
            if not messagebox.askyesno(
                APP_NAME,
                "変換に成功した元ファイルを削除します。\n"
                "削除した元ファイルは元に戻せません。\n\n"
                "続けますか？"
            ):
                return
        outdir=Path(self.uni_outdir.get().strip() or ".");outdir.mkdir(parents=True,exist_ok=True)
        fmt=self.uni_fmt.get().upper()
        extmap={"JPEG":"jpg","AAC":"aac","ICO":"ico"}
        ext=extmap.get(fmt,fmt.lower())
        image_out=fmt in {"PNG","JPEG","WEBP","BMP","TIFF","GIF","ICO"}
        audio_out=fmt in {"MP3","WAV","FLAC","M4A","AAC","OGG","OPUS"}
        files=list(self.uni_files)
        total=len(files)
        if hasattr(self,"uni_progress"):
            self.uni_progress["maximum"]=total or 1
            self.uni_progress["value"]=0
        if hasattr(self,"uni_percent"):
            self.uni_percent.config(text="0%")

        def _ui_uni_progress(done):
            try:
                self.uni_progress["value"]=done
                self.uni_percent.config(text=f"{round(done*100/total) if total else 0}%")
            except Exception:
                pass

        def worker():
            ok=0;fails=[];delete_fails=[];deleted_count=0
            for inp in files:
                out=outdir/(Path(inp).stem+"."+ext)

                # Do not overwrite the source when output directory/extension match.
                try:
                    if os.path.normcase(os.path.abspath(inp)) == os.path.normcase(os.path.abspath(str(out))):
                        out=outdir/(Path(inp).stem+"_converted."+ext)
                except Exception:
                    pass

                try:
                    if image_out:
                        # First try Pillow for ordinary still images.
                        try:
                            im=Image.open(inp)
                            if fmt=="JPEG":
                                im.convert("RGB").save(out,"JPEG",quality=95)
                            elif fmt=="ICO":
                                im.convert("RGBA").save(out,"ICO",
                                    sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
                            else:
                                im.save(out,fmt)
                        except Exception:
                            ff=tool("ffmpeg") or "ffmpeg"
                            r=subprocess.run([ff,"-y","-i",inp,str(out)],capture_output=True,text=True,
                                             creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
                            if r.returncode!=0: raise RuntimeError((r.stderr or "")[-800:])
                    else:
                        ff=tool("ffmpeg") or "ffmpeg"
                        cmd=[ff,"-y","-i",inp]
                        if audio_out:
                            cmd += ["-vn"]
                            if fmt=="MP3": cmd += ["-c:a","libmp3lame","-b:a","192k"]
                            elif fmt=="M4A": cmd += ["-c:a","aac","-b:a","192k"]
                            elif fmt=="AAC": cmd += ["-c:a","aac","-b:a","192k"]
                            elif fmt=="OPUS": cmd += ["-c:a","libopus","-b:a","160k"]
                            elif fmt=="OGG": cmd += ["-c:a","libvorbis","-q:a","5"]
                        else:
                            if fmt in {"MP4","MOV","MKV"}: cmd += ["-c:v","libx264","-c:a","aac"]
                            elif fmt=="WEBM": cmd += ["-c:v","libvpx-vp9","-c:a","libopus"]
                            elif fmt=="AVI": cmd += ["-c:v","mpeg4","-c:a","mp3"]
                        cmd += [str(out)]
                        r=subprocess.run(cmd,capture_output=True,text=True,
                                         creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
                        if r.returncode!=0: raise RuntimeError((r.stderr or "")[-800:])
                    ok+=1

                    if delete_originals:
                        if out.exists() and out.is_file() and out.stat().st_size > 0:
                            try:
                                Path(inp).unlink()
                                deleted_count+=1
                            except Exception as de:
                                delete_fails.append(f"{Path(inp).name}: {de}")
                        else:
                            delete_fails.append(
                                f"{Path(inp).name}: 出力ファイルを確認できないため元ファイルは削除しませんでした。"
                            )
                except Exception as e:
                    fails.append(f"{Path(inp).name}: {e}")

                try:
                    done=ok+len(fails)
                    self.root.after(0,_ui_uni_progress,done)
                except Exception:
                    pass

            msg=f"{ok}/{len(files)} 件変換しました。"
            if delete_originals:
                msg += f"\n元ファイル削除: {deleted_count} 件"
            if fails:
                msg += "\n\n変換失敗:\n"+"\n".join(fails[:5])
            if delete_fails:
                msg += "\n\n元ファイル削除失敗:\n"+"\n".join(delete_fails[:5])

            def show_result():
                if fails or delete_fails:
                    messagebox.showwarning(APP_NAME,msg)
                else:
                    messagebox.showinfo(APP_NAME,msg)
            self.root.after(0,show_result)
        threading.Thread(target=worker,daemon=True).start()

    # ---------- Video editor ----------
    def page_videoedit(self):
        p=self.p(); c=self.card(self.content); c.pack(fill="both",expand=True)
        tk.Label(c,text="動画編集",font=("Segoe UI",18,"bold"),bg=p["panel"],fg=p["text"]).pack(anchor="w",padx=20,pady=(18,6))
        tk.Label(c,text="カット / 回転 / ミュート / テロップ（文字） / 効果音の追加",
                 bg=p["panel"],fg=p["muted"]).pack(anchor="w",padx=20,pady=(0,10))
        self.ve_input=tk.StringVar(); self.ve_output=tk.StringVar()
        self.ve_start=tk.StringVar(value="00:00:00"); self.ve_end=tk.StringVar(value="")
        self.ve_rotate=tk.StringVar(value="なし"); self.ve_mute=tk.BooleanVar(value=False)
        self.ve_text=tk.StringVar(value="")
        self.ve_font=tk.StringVar(value="Yu Gothic")
        self.ve_fontsize=tk.StringVar(value="42")
        self.ve_text_x=tk.StringVar(value="40")
        self.ve_text_y=tk.StringVar(value="40")
        self.ve_text_color=tk.StringVar(value="white")
        self.ve_sfx=tk.StringVar(value="")
        self.ve_sfx_vol=tk.StringVar(value="0.6")
        self.ve_sfx_at=tk.StringVar(value="00:00:00")

        def file_row(title,var,save=False,audio=False):
            r=tk.Frame(c,bg=p["panel"]); r.pack(fill="x",padx=20,pady=4)
            tk.Label(r,text=title,width=12,anchor="w",bg=p["panel"],fg=p["text"]).pack(side="left")
            tk.Entry(r,textvariable=var,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",fill="x",expand=True,ipady=7,padx=(0,8))
            def choose():
                if save:
                    f=filedialog.asksaveasfilename(defaultextension=".mp4",filetypes=[("MP4","*.mp4")])
                elif audio:
                    f=filedialog.askopenfilename(filetypes=[("Audio","*.mp3 *.wav *.m4a *.aac *.ogg *.flac"),("All","*.*")])
                else:
                    f=filedialog.askopenfilename(filetypes=[("Video","*.mp4 *.mkv *.webm *.mov *.avi *.m4v *.ts *.mpg *.mpeg"),("All","*.*")])
                if f: var.set(f)
            b=ctk.CTkButton(r,text="参照",command=choose); self.style_button(b); b.pack(side="left")
        file_row("入力動画",self.ve_input)
        file_row("出力",self.ve_output,True)

        r=tk.Frame(c,bg=p["panel"]); r.pack(fill="x",padx=20,pady=6)
        for title,var in [("開始",self.ve_start),("終了",self.ve_end)]:
            tk.Label(r,text=title,bg=p["panel"],fg=p["text"]).pack(side="left",padx=(0,6))
            tk.Entry(r,textvariable=var,width=12,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",ipady=6,padx=(0,14))
        tk.Label(r,text="回転",bg=p["panel"],fg=p["text"]).pack(side="left")
        ttk.Combobox(r,textvariable=self.ve_rotate,state="readonly",values=["なし","右90°","左90°","180°"],width=10).pack(side="left",padx=8)
        tk.Checkbutton(r,text="音声を消す",variable=self.ve_mute,bg=p["panel"],fg=p["text"],selectcolor=p["panel2"],activebackground=p["panel"]).pack(side="left",padx=10)

        # Telop / text
        tcard=self.card(c); tcard.pack(fill="x",padx=20,pady=8)
        tk.Label(tcard,text="テロップ / 文字入れ",font=("Segoe UI",11,"bold"),bg=p["panel"],fg=p["text"]).pack(anchor="w",padx=12,pady=(10,6))
        r=tk.Frame(tcard,bg=p["panel"]); r.pack(fill="x",padx=12,pady=4)
        tk.Label(r,text="文字",bg=p["panel"],fg=p["text"],width=8,anchor="w").pack(side="left")
        tk.Entry(r,textvariable=self.ve_text,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",fill="x",expand=True,ipady=6)
        r=tk.Frame(tcard,bg=p["panel"]); r.pack(fill="x",padx=12,pady=4)
        tk.Label(r,text="フォント",bg=p["panel"],fg=p["text"]).pack(side="left")
        self.ve_font_box=ttk.Combobox(r,textvariable=self.ve_font,state="readonly",width=28)
        self.ve_font_box.pack(side="left",padx=6)
        try:
            fonts=self._list_system_fonts()
            self.ve_font_box["values"]=fonts
            if "Yu Gothic" in fonts: self.ve_font.set("Yu Gothic")
        except Exception:
            self.ve_font_box["values"]=["Yu Gothic","Meiryo","MS Gothic","Arial"]
        tk.Label(r,text="サイズ",bg=p["panel"],fg=p["text"]).pack(side="left",padx=(10,4))
        tk.Entry(r,textvariable=self.ve_fontsize,width=6,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",ipady=6)
        tk.Label(r,text="色",bg=p["panel"],fg=p["text"]).pack(side="left",padx=(10,4))
        ttk.Combobox(r,textvariable=self.ve_text_color,state="readonly",width=10,
                     values=["white","yellow","red","cyan","lime","black"]).pack(side="left")
        r=tk.Frame(tcard,bg=p["panel"]); r.pack(fill="x",padx=12,pady=(4,10))
        tk.Label(r,text="位置 X",bg=p["panel"],fg=p["text"]).pack(side="left")
        tk.Entry(r,textvariable=self.ve_text_x,width=6,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",ipady=6,padx=4)
        tk.Label(r,text="Y",bg=p["panel"],fg=p["text"]).pack(side="left")
        tk.Entry(r,textvariable=self.ve_text_y,width=6,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",ipady=6,padx=4)

        # SFX
        scard=self.card(c); scard.pack(fill="x",padx=20,pady=4)
        tk.Label(scard,text="効果音 / 追加音声",font=("Segoe UI",11,"bold"),bg=p["panel"],fg=p["text"]).pack(anchor="w",padx=12,pady=(10,6))
        file_row_parent=scard
        r=tk.Frame(scard,bg=p["panel"]); r.pack(fill="x",padx=12,pady=4)
        tk.Label(r,text="効果音",width=8,anchor="w",bg=p["panel"],fg=p["text"]).pack(side="left")
        tk.Entry(r,textvariable=self.ve_sfx,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",fill="x",expand=True,ipady=6,padx=(0,8))
        def choose_sfx():
            f=filedialog.askopenfilename(filetypes=[("Audio","*.mp3 *.wav *.m4a *.aac *.ogg *.flac"),("All","*.*")])
            if f: self.ve_sfx.set(f)
        b=ctk.CTkButton(r,text="参照",command=choose_sfx); self.style_button(b); b.pack(side="left")
        r=tk.Frame(scard,bg=p["panel"]); r.pack(fill="x",padx=12,pady=(4,10))
        tk.Label(r,text="音量(0-1)",bg=p["panel"],fg=p["text"]).pack(side="left")
        tk.Entry(r,textvariable=self.ve_sfx_vol,width=6,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",ipady=6,padx=6)
        tk.Label(r,text="開始時刻",bg=p["panel"],fg=p["text"]).pack(side="left",padx=(12,4))
        tk.Entry(r,textvariable=self.ve_sfx_at,width=12,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",ipady=6)

        note=tk.Label(c,text="プレビューで内容を確認してから保存してください。",bg=p["panel"],fg=p["muted"],font=("Segoe UI",9))
        note.pack(anchor="w",padx=20,pady=(6,4))
        br=tk.Frame(c,bg=p["panel"]); br.pack(anchor="w",padx=20,pady=(0,16))
        tk.Button(br,text="▶ プレビュー再生",command=self._video_preview,bg=p["panel2"],fg=p["text"],relief="flat",bd=0,padx=12,pady=7).pack(side="left")
        tk.Button(br,text="■ 再生停止",command=self._video_preview_stop,bg=p["panel2"],fg=p["text"],relief="flat",bd=0,padx=12,pady=7).pack(side="left",padx=6)
        tk.Button(br,text="💾 保存",command=self._videoedit_run,bg=p["accent"],fg="white",relief="flat",bd=0,padx=12,pady=7).pack(side="left")

    def _video_preview(self):
        inp=self.ve_input.get().strip()
        if not inp:return messagebox.showwarning(APP_NAME,"入力動画を選んでください。")
        ffplay=tool("ffplay")
        if not ffplay:return messagebox.showerror(APP_NAME,"ffplay が見つかりません。")
        self._video_preview_stop()
        cmd=[ffplay,"-autoexit","-window_title","ATRAC 動画プレビュー"]
        if self.ve_start.get().strip():cmd+=["-ss",self.ve_start.get().strip()]
        cmd.append(inp)
        try:self.ve_preview_proc=self._track_proc(subprocess.Popen(cmd,creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0)))
        except Exception as e:messagebox.showerror(APP_NAME,str(e))

    def _video_preview_stop(self):
        p=getattr(self,"ve_preview_proc",None)
        self.ve_preview_proc=None
        self._kill_process(p, timeout=2.0)

    def _ve_secs(self,t):
        a=[float(x) for x in str(t).strip().split(":")]
        return a[-1]+(a[-2]*60 if len(a)>1 else 0)+(a[-3]*3600 if len(a)>2 else 0)

    def _videoedit_run(self):
        inp=self.ve_input.get().strip()
        if not inp: return messagebox.showwarning(APP_NAME,"入力動画を選んでください。")
        out=self.ve_output.get().strip() or str(Path(inp).with_name(Path(inp).stem+"_edited.mp4"))
        ff=tool("ffmpeg") or "ffmpeg"
        cmd=[ff,"-y"]
        if self.ve_start.get().strip():
            cmd += ["-ss",self.ve_start.get().strip()]
        cmd += ["-i",inp]
        sfx=self.ve_sfx.get().strip()
        has_sfx=bool(sfx and os.path.isfile(sfx))
        if has_sfx:
            cmd += ["-i",sfx]

        # duration trim
        if self.ve_end.get().strip():
            if self.ve_start.get().strip():
                try:
                    cmd += ["-t",str(max(0.01,self._ve_secs(self.ve_end.get().strip())-self._ve_secs(self.ve_start.get().strip())))]
                except Exception:
                    cmd += ["-to",self.ve_end.get().strip()]
            else:
                cmd += ["-to",self.ve_end.get().strip()]

        vf=[]
        rot=self.ve_rotate.get()
        if rot=="右90°": vf.append("transpose=1")
        elif rot=="左90°": vf.append("transpose=2")
        elif rot=="180°": vf.append("hflip,vflip")

        txt=(self.ve_text.get() or "").strip()
        if txt:
            font=self._find_system_font_file(self.ve_font.get()) or ""
            # escape for ffmpeg filter
            def esc(s):
                return s.replace("\\","\\\\").replace(":","\\:").replace("'","\\'")
            fsize=max(10,int(self.ve_fontsize.get() or 42))
            x=self.ve_text_x.get().strip() or "40"
            y=self.ve_text_y.get().strip() or "40"
            color=self.ve_text_color.get().strip() or "white"
            dt=f"drawtext=text='{esc(txt)}':fontsize={fsize}:fontcolor={color}:x={x}:y={y}:borderw=2:bordercolor=black"
            if font:
                dt += f":fontfile='{esc(font)}'"
            vf.append(dt)

        fc=[]
        maps=[]
        if vf:
            cmd += ["-vf",",".join(vf)]

        if has_sfx and not self.ve_mute.get():
            try:
                vol=float(self.ve_sfx_vol.get() or 0.6)
            except Exception:
                vol=0.6
            try:
                delay_ms=int(self._ve_secs(self.ve_sfx_at.get() or "0")*1000)
            except Exception:
                delay_ms=0
            # [0:a] original, [1:a] sfx delayed
            fc.append(f"[1:a]volume={vol},adelay={delay_ms}|{delay_ms}[sfx]")
            fc.append(f"[0:a][sfx]amix=inputs=2:duration=first:dropout_transition=0[aout]")
            cmd += ["-filter_complex",";".join(fc),"-map","0:v","-map","[aout]"]
        elif self.ve_mute.get():
            cmd += ["-an"]
        else:
            cmd += ["-c:a","aac","-b:a","192k"]

        cmd += ["-c:v","libx264","-preset","fast","-crf","20",out]
        self._run_media_task(cmd,"動画編集",out)


    def page_gain(self):
        p=self.p(); c=self.card(self.content); c.pack(fill="both",expand=True)
        tk.Label(c,text="音量調整（MP3 / M4A / FLAC / WAV / MP4 など）",font=("Segoe UI",18,"bold"),bg=p["panel"],fg=p["text"]).pack(anchor="w",padx=20,pady=(18,8))
        tk.Label(c,text="音楽・動画の音量を手動で増減、または自動ノーマライズします。手動ゲインのスライダーを動かすと自動で「手動 dB」になります。元ファイルは変更せず別ファイルに保存します。",
                 wraplength=780,justify="left",bg=p["panel"],fg=p["muted"]).pack(anchor="w",padx=20,pady=(0,12))
        self.gain_input=tk.StringVar(); self.gain_output=tk.StringVar(); self.gain_files=[]; self.gain_overwrite=tk.BooleanVar(value=False)
        self.gain_mode=tk.StringVar(value="自動ノーマライズ")
        self.gain_db=tk.DoubleVar(value=0.0)

        for title,var,save in [("入力",self.gain_input,False),("出力",self.gain_output,True)]:
            r=tk.Frame(c,bg=p["panel"]);r.pack(fill="x",padx=20,pady=5)
            tk.Label(r,text=title,width=8,anchor="w",bg=p["panel"],fg=p["text"]).pack(side="left")
            tk.Entry(r,textvariable=var,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat").pack(side="left",fill="x",expand=True,ipady=7)
            def choose(v=var,sv=save):
                if sv:
                    inp=self.gain_input.get().strip()
                    ext=Path(inp).suffix.lower() if inp else ".mp3"
                    f=filedialog.asksaveasfilename(defaultextension=ext,filetypes=[("Audio/Video","*.mp3 *.m4a *.aac *.flac *.wav *.ogg *.opus *.mp4 *.m4v *.mov"),("All","*.*")])
                else:
                    f=filedialog.askopenfilename(filetypes=[("Audio/Video","*.mp3 *.m4a *.aac *.flac *.wav *.ogg *.opus *.mp4 *.m4v *.mov"),("All","*.*")])
                if f:v.set(f)
            tk.Button(r,text="参照",command=choose,bg=p["panel2"],fg=p["text"],relief="flat",bd=0,padx=10,pady=6).pack(side="left",padx=6)

        r=tk.Frame(c,bg=p["panel"]);r.pack(fill="x",padx=20,pady=10)
        tk.Label(r,text="方式",bg=p["panel"],fg=p["text"]).pack(side="left")
        ttk.Combobox(r,textvariable=self.gain_mode,state="readonly",
                     values=["自動ノーマライズ","手動 dB"],width=18).pack(side="left",padx=8)
        tk.Label(r,text="手動ゲイン",bg=p["panel"],fg=p["text"]).pack(side="left",padx=(14,0))
        tk.Scale(r,from_=-12,to=12,resolution=.5,orient="horizontal",variable=self.gain_db,length=260,
                 bg=p["panel"],fg=p["text"],highlightthickness=0).pack(side="left",padx=5)
        self.root.after(300,lambda:self.gain_db.trace_add("write",lambda *a:self.gain_mode.set("手動 dB")))
        tk.Label(c,text="自動ノーマライズ: EBU R128 loudnorm（目標 -16 LUFS） / 手動: -12 ～ +12 dB",
                 bg=p["panel"],fg=p["muted"]).pack(anchor="w",padx=20,pady=(0,8))
        opts=tk.Frame(c,bg=p["panel"]);opts.pack(fill="x",padx=20,pady=(4,4))
        tk.Checkbutton(opts,text="元ファイルを変更（上書き）",variable=self.gain_overwrite,
                       bg=p["panel"],fg=p["text"],selectcolor=p["panel2"]).pack(side="left")
        tk.Label(opts,text="※ 上書き時は一時ファイルで処理してから置き換えます。",bg=p["panel"],fg=p["muted"]).pack(side="left",padx=8)

        batch=tk.Frame(c,bg=p["panel"]);batch.pack(fill="x",padx=20,pady=(4,8))
        tk.Button(batch,text="複数ファイル追加",command=self._gain_add_files,bg=p["panel2"],fg=p["text"],relief="flat",bd=0,padx=12,pady=7).pack(side="left")
        tk.Button(batch,text="一括音量調整",command=self._gain_run_batch,bg=p["accent"],fg="white",relief="flat",bd=0,padx=12,pady=7).pack(side="left",padx=6)
        self.gain_batch_label=tk.Label(batch,text="0 ファイル",bg=p["panel"],fg=p["muted"]);self.gain_batch_label.pack(side="left",padx=8)

        tk.Button(c,text="🔊 1ファイルを音量調整",command=self._gain_run,bg=p["accent"],fg="white",
                  activebackground=p["accent2"],activeforeground="white",relief="flat",bd=0,padx=16,pady=9).pack(anchor="w",padx=20,pady=12)

    def _gain_add_files(self):
        fs=filedialog.askopenfilenames(filetypes=[("Audio/Video","*.mp3 *.m4a *.aac *.flac *.wav *.ogg *.opus *.mp4 *.m4v *.mov"),("All","*.*")])
        if fs:
            self.gain_files=list(fs)
            if hasattr(self,"gain_batch_label"):self.gain_batch_label.config(text=f"{len(self.gain_files)} ファイル")

    def _gain_src_rate(self,inp):
        try:
            fp=tool("ffprobe")
            if fp:
                out=subprocess.run([fp,"-v","error","-select_streams","a:0","-show_entries","stream=sample_rate",
                                    "-of","default=nw=1:nk=1",inp],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,
                                   text=True,creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0)).stdout.strip()
                if out.isdigit(): return int(out)
        except Exception:
            pass
        return 44100

    def _gain_filter(self,inp):
        """Manual: volume (+limiter when boosting). Auto: two-pass EBU R128 loudnorm."""
        if self.gain_mode.get()!="自動ノーマライズ":
            g=float(self.gain_db.get())
            f=f"volume={g:+.1f}dB"
            if g>0: f+=",alimiter=limit=0.97"
            return f
        base="loudnorm=I=-16:TP=-1.5:LRA=11"
        sr=self._gain_src_rate(inp)
        ff=tool("ffmpeg")
        try:
            r=subprocess.run([ff,"-hide_banner","-nostats","-i",inp,"-vn","-af",base+":print_format=json","-f","null","-"],
                             stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True,encoding="utf-8",errors="replace",
                             creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
            d=json.loads(re.findall(r"\{[^{}]*\}",r.stderr,re.S)[-1])
            return (f"{base}:measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}"
                    f":measured_thresh={d['input_thresh']}:offset={d['target_offset']}:linear=true,aresample={sr}")
        except Exception:
            return base+f",aresample={sr}"

    def _gain_build_cmd(self,inp,out,af=None):
        ext=Path(inp).suffix.lower()
        ff=tool("ffmpeg")
        if not ff: raise RuntimeError("FFmpeg が見つかりません。")
        if af is None: af=self._gain_filter(inp)
        cmd=[ff,"-y","-hide_banner","-i",inp,"-map_metadata","0"]
        art=["-map","0:a:0","-map","0:v:0?","-c:v","copy"]
        if ext==".mp3":
            cmd += art+["-af",af,"-c:a","libmp3lame","-b:a","320k","-id3v2_version","3",out]
        elif ext in (".mp4",".m4v",".mov"):
            cmd += ["-map","0:v:0?","-map","0:a:0?","-c:v","copy","-af",af,"-c:a","aac","-b:a","256k","-movflags","+faststart",out]
        elif ext==".m4a":
            cmd += art+["-disposition:v:0","attached_pic","-af",af,"-c:a","aac","-b:a","256k","-movflags","+faststart",out]
        elif ext==".aac":
            cmd += ["-vn","-af",af,"-c:a","aac","-b:a","256k","-f","adts",out]
        elif ext==".flac":
            cmd += art+["-af",af,"-c:a","flac",out]
        elif ext==".wav":
            cmd += ["-vn","-af",af,"-c:a","pcm_s16le",out]
        elif ext==".ogg":
            cmd += ["-vn","-af",af,"-c:a","libvorbis","-q:a","6",out]
        elif ext==".opus":
            cmd += ["-vn","-af",af,"-c:a","libopus","-b:a","192k",out]
        else:
            raise ValueError("対応形式: MP3 / M4A / AAC / FLAC / WAV / OGG / OPUS / MP4 / M4V / MOV")
        return cmd

    def _gain_process_one_sync(self,inp,out,overwrite=False):
        import tempfile
        target=Path(inp) if overwrite else Path(out)
        if overwrite:
            fd,tmp=tempfile.mkstemp(prefix="atrac_gain_",suffix=Path(inp).suffix)
            os.close(fd)
            tmp_path=Path(tmp)
        else:
            tmp_path=target
        try:
            cmd=self._gain_build_cmd(inp,str(tmp_path))
            flags=getattr(subprocess,"CREATE_NO_WINDOW",0)
            r=subprocess.run(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True,encoding="utf-8",errors="replace",creationflags=flags)
            if r.returncode!=0:
                raise RuntimeError((r.stderr or "FFmpeg error")[-1800:])
            if overwrite:
                shutil.move(str(tmp_path),str(target))
            return str(target)
        finally:
            if overwrite and tmp_path.exists():
                try:tmp_path.unlink()
                except Exception:pass

    def _gain_run(self):
        inp=self.gain_input.get().strip()
        if not inp:return messagebox.showwarning(APP_NAME,"ファイルを選んでください。")
        overwrite=bool(self.gain_overwrite.get())
        ext=Path(inp).suffix.lower()
        out=self.gain_output.get().strip() or str(Path(inp).with_name(Path(inp).stem+"_gain"+ext))
        if overwrite: out=inp
        def worker():
            try:
                result=self._gain_process_one_sync(inp,out,overwrite)
                self.root.after(0,lambda:messagebox.showinfo(APP_NAME,"音量調整が完了しました。\n"+result))
            except Exception as e:
                self.root.after(0,lambda e=e:messagebox.showerror(APP_NAME,"音量調整エラー:\n"+str(e)))
        threading.Thread(target=worker,daemon=True).start()

    def _gain_run_batch(self):
        files=list(getattr(self,"gain_files",[]) or [])
        if not files:return messagebox.showwarning(APP_NAME,"「複数ファイル追加」でファイルを選んでください。")
        overwrite=bool(self.gain_overwrite.get())
        def worker():
            ok=0; errors=[]
            for inp in files:
                try:
                    ext=Path(inp).suffix.lower()
                    out=inp if overwrite else str(Path(inp).with_name(Path(inp).stem+"_gain"+ext))
                    self._gain_process_one_sync(inp,out,overwrite)
                    ok+=1
                    self.root.after(0,lambda n=ok:self.gain_batch_label.config(text=f"{n}/{len(files)} 完了"))
                except Exception as e:
                    errors.append(f"{Path(inp).name}: {e}")
            def done():
                msg=f"{ok}/{len(files)} ファイル完了"
                if errors: msg+="\n\n失敗:\n"+"\n".join(errors[:8])
                messagebox.showinfo(APP_NAME,msg)
            self.root.after(0,done)
        threading.Thread(target=worker,daemon=True).start()

    # ---------- Video compression ----------
    def page_compress(self):
        p=self.p(); c=self.card(self.content); c.pack(fill="both",expand=True)
        tk.Label(c,text="動画圧縮",font=("Segoe UI",18,"bold"),bg=p["panel"],fg=p["text"]).pack(anchor="w",padx=20,pady=(18,12))
        self.comp_input=tk.StringVar(); self.comp_output=tk.StringVar()
        self.comp_quality=tk.StringVar(value="標準 (CRF 23)"); self.comp_res=tk.StringVar(value="元の解像度")
        for title,var,save in [("入力",self.comp_input,False),("出力",self.comp_output,True)]:
            r=tk.Frame(c,bg=p["panel"]);r.pack(fill="x",padx=20,pady=6)
            tk.Label(r,text=title,width=10,anchor="w",bg=p["panel"],fg=p["text"]).pack(side="left")
            tk.Entry(r,textvariable=var,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",fill="x",expand=True,ipady=8,padx=(0,8))
            def choose(v=var,s=save):
                f=(filedialog.asksaveasfilename(defaultextension=".mp4",filetypes=[("MP4","*.mp4")]) if s else filedialog.askopenfilename(filetypes=[("Video","*.mp4 *.mkv *.webm *.mov *.avi"),("All","*.*")]))
                if f:v.set(f)
            b=ctk.CTkButton(r,text="参照",command=choose);self.style_button(b);b.pack(side="left")
        r=tk.Frame(c,bg=p["panel"]);r.pack(fill="x",padx=20,pady=12)
        tk.Label(r,text="圧縮率",bg=p["panel"],fg=p["text"]).pack(side="left")
        ttk.Combobox(r,textvariable=self.comp_quality,state="readonly",
                     values=["高画質 (CRF 18)","標準 (CRF 23)","小さめ (CRF 28)","最小 (CRF 32)"],width=18).pack(side="left",padx=8)
        tk.Label(r,text="解像度",bg=p["panel"],fg=p["text"]).pack(side="left",padx=(18,0))
        ttk.Combobox(r,textvariable=self.comp_res,state="readonly",
                     values=["元の解像度","1080p","720p","480p"],width=14).pack(side="left",padx=8)
        b=ctk.CTkButton(c,text="圧縮開始",command=self._compress_run);self.style_button(b,True);b.pack(anchor="w",padx=20,pady=18)

    def _compress_run(self):
        inp=self.comp_input.get().strip()
        if not inp:return messagebox.showwarning(APP_NAME,"入力動画を選んでください。")
        out=self.comp_output.get().strip() or str(Path(inp).with_name(Path(inp).stem+"_compressed.mp4"))
        crf={"高画質 (CRF 18)":"18","標準 (CRF 23)":"23","小さめ (CRF 28)":"28","最小 (CRF 32)":"32"}[self.comp_quality.get()]
        cmd=[tool("ffmpeg") or "ffmpeg","-y","-i",inp]
        h={"1080p":"1080","720p":"720","480p":"480"}.get(self.comp_res.get())
        if h: cmd += ["-vf",f"scale=-2:{h}"]
        cmd += ["-c:v","libx264","-preset","medium","-crf",crf,"-c:a","aac","-b:a","128k","-movflags","+faststart",out]
        self._run_media_task(cmd,"動画圧縮",out)

    # ---------- DVD ----------
    def page_dvd(self):
        p=self.p(); c=self.card(self.content); c.pack(fill="both",expand=True)
        tk.Label(c,text="DVD作成",font=("Segoe UI",18,"bold"),bg=p["panel"],fg=p["text"]).pack(anchor="w",padx=20,pady=(18,10))
        tk.Label(c,text="動画をDVD-Video向けのMPEG-2形式に変換します。VIDEO_TS作成には dvdauthor が必要です。",
                 wraplength=760,justify="left",bg=p["panel"],fg=p["muted"]).pack(anchor="w",padx=20,pady=(0,12))
        self.dvd_input=tk.StringVar(); self.dvd_folder=tk.StringVar(value=os.path.join(os.path.expanduser("~"),"Videos","DVD"))
        for title,var,isfolder in [("動画",self.dvd_input,False),("出力フォルダ",self.dvd_folder,True)]:
            r=tk.Frame(c,bg=p["panel"]);r.pack(fill="x",padx=20,pady=6)
            tk.Label(r,text=title,width=12,anchor="w",bg=p["panel"],fg=p["text"]).pack(side="left")
            tk.Entry(r,textvariable=var,bg=p["entry"],fg=p["text"],insertbackground=p["text"],relief="flat",bd=0).pack(side="left",fill="x",expand=True,ipady=8,padx=(0,8))
            def choose(v=var,folder=isfolder):
                f=filedialog.askdirectory() if folder else filedialog.askopenfilename(filetypes=[("Video","*.mp4 *.mkv *.mov *.avi *.webm"),("All","*.*")])
                if f:v.set(f)
            b=ctk.CTkButton(r,text="参照",command=choose);self.style_button(b);b.pack(side="left")
        b=ctk.CTkButton(c,text="DVD用ファイルを作成",command=self._dvd_run);self.style_button(b,True);b.pack(anchor="w",padx=20,pady=18)

    def _dvd_run(self):
        inp=self.dvd_input.get().strip(); folder=self.dvd_folder.get().strip()
        if not inp:return messagebox.showwarning(APP_NAME,"動画を選んでください。")
        Path(folder).mkdir(parents=True,exist_ok=True)
        mpg=str(Path(folder)/"dvd_video.mpg")
        cmd=[tool("ffmpeg") or "ffmpeg","-y","-i",inp,
             "-target","ntsc-dvd","-aspect","16:9","-c:v","mpeg2video","-c:a","ac3",mpg]
        def after():
            dv=tool("dvdauthor")
            if dv:
                video_ts=Path(folder)/"VIDEO_TS"; video_ts.mkdir(exist_ok=True)
                try:
                    subprocess.run([dv,"-o",folder,"-t",mpg],check=True,creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
                    subprocess.run([dv,"-o",folder,"-T"],check=True,creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
                    self.root.after(0,lambda:messagebox.showinfo(APP_NAME,"DVD-Videoフォルダを作成しました。"))
                except Exception as e:
                    self.root.after(0,lambda:messagebox.showwarning(APP_NAME,"MPEG-2は作成できましたがVIDEO_TS作成に失敗しました。\n"+str(e)))
            else:
                self.root.after(0,lambda:messagebox.showinfo(APP_NAME,"DVD互換MPEG-2を作成しました。\nVIDEO_TS作成には dvdauthor をインストールしてください。"))
        self._run_media_task(cmd,"DVD用動画作成",mpg,after)

    def _run_media_task(self,cmd,title,out,after=None):
        def worker():
            try:
                r=subprocess.run(cmd,capture_output=True,text=True,creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
                if r.returncode!=0: raise RuntimeError((r.stderr or r.stdout)[-1800:])
                if after: after()
                else:self.root.after(0,lambda:messagebox.showinfo(APP_NAME,f"{title}が完了しました。\n{out}"))
            except Exception as e:
                self.root.after(0,lambda:messagebox.showerror(APP_NAME,f"{title}に失敗しました。\n{e}"))
        threading.Thread(target=worker,daemon=True).start()

    def page_format(self):
        p=self.p()
        c=self.card(self.content);c.pack(fill="both",expand=True)
        tk.Label(c,text=self.tr("format_title"),font=("Segoe UI",16,"bold"),
                 bg=p["panel"],fg=p["text"]).pack(anchor="w",padx=18,pady=(16,8))
        tk.Label(c,text=self.tr("format_warning"),font=("Segoe UI",10,"bold"),
                 bg=p["panel"],fg=p["danger"] if "danger" in p else p["text"],
                 wraplength=760,justify="left").pack(anchor="w",padx=18,pady=(0,14))

        self.format_drive=tk.StringVar(value="")
        self.format_fs=tk.StringVar(value="exFAT")
        self.format_label=tk.StringVar(value="")

        row=tk.Frame(c,bg=p["panel"]);row.pack(fill="x",padx=18,pady=6)
        tk.Label(row,text=self.tr("format_drive"),bg=p["panel"],fg=p["text"],width=18,anchor="w").pack(side="left")
        self.format_drive_box=ttk.Combobox(row,textvariable=self.format_drive,state="readonly",width=42)
        self.format_drive_box.pack(side="left",padx=(0,8))
        b=ctk.CTkButton(row,text=self.tr("format_refresh"),command=self._format_refresh_drives);self.style_button(b);b.pack(side="left")

        row=tk.Frame(c,bg=p["panel"]);row.pack(fill="x",padx=18,pady=6)
        tk.Label(row,text=self.tr("format_fs"),bg=p["panel"],fg=p["text"],width=18,anchor="w").pack(side="left")
        ttk.Combobox(row,textvariable=self.format_fs,values=(["FAT32","exFAT","APFS"] if sys.platform=="darwin" else ["FAT32","exFAT","NTFS"]),state="readonly",width=18).pack(side="left")

        row=tk.Frame(c,bg=p["panel"]);row.pack(fill="x",padx=18,pady=6)
        tk.Label(row,text=self.tr("format_label"),bg=p["panel"],fg=p["text"],width=18,anchor="w").pack(side="left")
        tk.Entry(row,textvariable=self.format_label,bg=p["entry"],fg=p["text"],insertbackground=p["text"],
                 relief="flat",bd=0,width=28).pack(side="left",ipady=7)

        b=ctk.CTkButton(c,text=self.tr("format_start"),command=self._format_start)
        self.style_button(b,True);b.pack(anchor="w",padx=18,pady=(12,10))

        self.format_status=tk.StringVar(value="")
        tk.Label(c,textvariable=self.format_status,bg=p["panel"],fg=p["muted"],
                 wraplength=760,justify="left").pack(anchor="w",padx=18,pady=(4,12))

        self._format_refresh_drives()

    def _format_refresh_drives(self):
        drives=[]; self._format_device_map={}
        if sys.platform=="darwin":
            try:
                r=subprocess.run(["/usr/sbin/diskutil","list","-plist","external","physical"],capture_output=True)
                if r.returncode==0:
                    data=plistlib.loads(r.stdout)
                    for d in data.get("AllDisks",[]):
                        dev="/dev/"+str(d)
                        ir=subprocess.run(["/usr/sbin/diskutil","info","-plist",dev],capture_output=True)
                        if ir.returncode!=0:continue
                        info=plistlib.loads(ir.stdout)
                        if info.get("Internal",False):continue
                        size=float(info.get("TotalSize") or 0)/(1024**3)
                        name=info.get("MediaName") or info.get("IOKitRegistryEntryName") or "External disk"
                        label=f"{dev}  ({size:.1f} GB)  {name}"
                        drives.append(label); self._format_device_map[label]=dev
            except Exception:pass
        else:
            import string,ctypes
            DRIVE_REMOVABLE=2; system_drive=(os.environ.get("SystemDrive") or "C:").upper()
            for letter in string.ascii_uppercase:
                root=letter+":\\"
                try:dtype=ctypes.windll.kernel32.GetDriveTypeW(root)
                except Exception:continue
                if dtype!=DRIVE_REMOVABLE:continue
                drive=(letter+":").upper()
                if drive==system_drive:continue
                try:
                    total=ctypes.c_ulonglong(0);free=ctypes.c_ulonglong(0)
                    ok=ctypes.windll.kernel32.GetDiskFreeSpaceExW(root,None,ctypes.byref(total),ctypes.byref(free))
                    label=f"{drive}  ({total.value/(1024**3):.1f} GB)" if ok else drive
                except Exception:label=drive
                drives.append(label);self._format_device_map[label]=drive
        try:
            self.format_drive_box["values"]=drives
            self.format_drive.set(drives[0] if drives else "")
        except Exception:pass

    def _format_start(self):
        selected=self.format_drive.get().strip()
        if not selected:
            return messagebox.showwarning(APP_NAME,"USBメモリまたはSDカードを選んでください。" if self.lang=="ja" else "Select a removable USB/SD drive.")
        fs=self.format_fs.get().strip(); label=(self.format_label.get().strip()[:32] or "UNTITLED")
        device=getattr(self,"_format_device_map",{}).get(selected,selected.split()[0])
        if sys.platform=="darwin":
            if not re.match(r"^/dev/disk\d+$",device):return messagebox.showerror(APP_NAME,self.tr("format_blocked"))
            try:
                ir=subprocess.run(["/usr/sbin/diskutil","info","-plist",device],capture_output=True)
                info=plistlib.loads(ir.stdout) if ir.returncode==0 else {}
                rootinfo=subprocess.run(["/usr/sbin/diskutil","info","-plist","/"],capture_output=True)
                rinfo=plistlib.loads(rootinfo.stdout) if rootinfo.returncode==0 else {}
                rootdisk=str(rinfo.get("ParentWholeDisk") or rinfo.get("DeviceIdentifier") or "")
                if info.get("Internal",True) or device.endswith(rootdisk):return messagebox.showerror(APP_NAME,self.tr("format_blocked"))
            except Exception:return messagebox.showerror(APP_NAME,self.tr("format_blocked"))
            msg=(f"{device} を {fs} でフォーマットします。\nこのディスクのデータはすべて消去されます。\n\n続行しますか？" if self.lang=="ja" else f"Format {device} as {fs}?\nAll data on this disk will be erased.\n\nContinue?")
            if not messagebox.askyesno(APP_NAME,msg,icon="warning"):return
            fmtmap={"FAT32":("FAT32","MBRFormat"),"exFAT":("ExFAT","MBRFormat"),"APFS":("APFS","GPTFormat")}
            if fs not in fmtmap:return messagebox.showerror(APP_NAME,"macOSではこのファイルシステムに対応していません。" if self.lang=="ja" else "This filesystem is not supported by macOS formatting.")
            fmt,scheme=fmtmap[fs]; cmd=["/usr/sbin/diskutil","eraseDisk",fmt,label,scheme,device]
        else:
            import ctypes
            drive=str(device).upper(); system_drive=(os.environ.get("SystemDrive") or "C:").upper()
            if drive==system_drive or not re.match(r"^[A-Z]:$",drive):return messagebox.showerror(APP_NAME,self.tr("format_blocked"))
            try:dtype=ctypes.windll.kernel32.GetDriveTypeW(drive+"\\")
            except Exception:dtype=0
            if dtype!=2:return messagebox.showerror(APP_NAME,self.tr("format_blocked"))
            msg=(f"{drive} を {fs} でフォーマットします。\nこのドライブのデータはすべて消去されます。\n\n続行しますか？" if self.lang=="ja" else f"Format {drive} as {fs}?\nAll data on this drive will be erased.\n\nContinue?")
            if not messagebox.askyesno(APP_NAME,msg,icon="warning"):return
            if fs=="FAT32":
                safe_label=label.replace("'","''"); ps_cmd=("$ErrorActionPreference='Stop';"+f"Format-Volume -DriveLetter '{drive[0]}' -FileSystem FAT32 -NewFileSystemLabel '{safe_label}' -Confirm:$false -Force")
                cmd=["powershell.exe","-NoProfile","-ExecutionPolicy","Bypass","-Command",ps_cmd]
            else:
                cmd=["format.com",drive,"/FS:"+fs,"/Q","/Y","/V:"+label]
        self.format_status.set("フォーマット中..." if self.lang=="ja" else "Formatting...")
        def run_format():
            try:
                r=subprocess.run(cmd,capture_output=True,text=True,creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
                if r.returncode!=0:raise RuntimeError(((r.stdout or "")+"\n"+(r.stderr or ""))[-1600:])
                self.root.after(0,lambda:self.format_status.set(self.tr("format_done")));self.root.after(0,self._format_refresh_drives)
            except Exception as e:self.root.after(0,lambda:messagebox.showerror(APP_NAME,("フォーマットに失敗しました。\n\n" if self.lang=="ja" else "Format failed.\n\n")+str(e)))
        threading.Thread(target=run_format,daemon=True).start()

    def page_calculator(self):
        p=self.p()
        c=self.card(self.content);c.pack(fill="x")
        tk.Label(c,text=self.tr("calc_title"),font=("Segoe UI",16,"bold"),
                 bg=p["panel"],fg=p["text"]).pack(anchor="w",padx=18,pady=(16,10))

        self.calc_var=tk.StringVar(value="")
        ent=tk.Entry(c,textvariable=self.calc_var,font=("Consolas",20),
                     justify="right",relief="flat",bd=0,bg=p["entry"],fg=p["text"],
                     insertbackground=p["text"])
        ent.pack(fill="x",padx=18,pady=(0,12),ipady=10)
        ent.focus_set()

        grid=tk.Frame(c,bg=p["panel"]);grid.pack(fill="x",padx=18,pady=(0,18))
        keys=[
            ["7","8","9","/","("],
            ["4","5","6","*",")"],
            ["1","2","3","-","√"],
            ["0",".","%","+","="]
        ]
        for r,row in enumerate(keys):
            grid.grid_rowconfigure(r,weight=1)
            for col,k in enumerate(row):
                grid.grid_columnconfigure(col,weight=1)
                b=ctk.CTkButton(grid,text=k,font=("Segoe UI",12,"bold"),
                            command=lambda x=k:self._calc_press(x))
                self.style_button(b, k=="=")
                b.grid(row=r,column=col,sticky="nsew",padx=3,pady=3,ipady=7)

        actions=tk.Frame(c,bg=p["panel"]);actions.pack(fill="x",padx=18,pady=(0,18))
        b=ctk.CTkButton(actions,text=self.tr("calc_clear"),command=lambda:self.calc_var.set(""))
        self.style_button(b);b.pack(side="left")
        b=ctk.CTkButton(actions,text=self.tr("calc_back"),command=lambda:self.calc_var.set(self.calc_var.get()[:-1]))
        self.style_button(b);b.pack(side="left",padx=8)

        ent.bind("<Return>",lambda e:self._calc_press("="))
        ent.bind("<Escape>",lambda e:self.calc_var.set(""))

    def _calc_press(self,key):
        if key=="=":
            expr=self.calc_var.get().strip()
            if not expr:return
            try:
                # Safe arithmetic-only evaluator.
                import ast, operator
                ops={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,
                     ast.Div:operator.truediv,ast.Mod:operator.mod,ast.Pow:operator.pow,
                     ast.USub:operator.neg,ast.UAdd:operator.pos}
                def ev(n):
                    if isinstance(n,ast.Expression):return ev(n.body)
                    if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)):return n.value
                    if isinstance(n,ast.BinOp) and type(n.op) in ops:return ops[type(n.op)](ev(n.left),ev(n.right))
                    if isinstance(n,ast.UnaryOp) and type(n.op) in ops:return ops[type(n.op)](ev(n.operand))
                    raise ValueError
                val=ev(ast.parse(expr,mode="eval"))
                if isinstance(val,float) and val.is_integer():val=int(val)
                self.calc_var.set(str(val))
            except Exception:
                self.calc_var.set(self.tr("calc_error"))
        elif key=="√":
            try:
                v=float(self.calc_var.get())
                if v<0:raise ValueError
                out=math.sqrt(v)
                self.calc_var.set(str(int(out) if out.is_integer() else out))
            except Exception:
                self.calc_var.set(self.tr("calc_error"))
        else:
            if self.calc_var.get()==self.tr("calc_error"):
                self.calc_var.set("")
            self.calc_var.set(self.calc_var.get()+key)


    def page_player(self):
        p=self.p()
        c=self.card(self.content); c.pack(fill="both", expand=True)
        tk.Label(c,text=self.tr("player_title"),font=("Segoe UI",16,"bold"),bg=p["panel"],fg=p["text"]).pack(anchor="w",padx=18,pady=(16,4))
        tk.Label(c,text=self.tr("player_hint"),font=("Segoe UI",9),bg=p["panel"],fg=p["muted"]).pack(anchor="w",padx=18,pady=(0,10))

        row=tk.Frame(c,bg=p["panel"]); row.pack(fill="x", padx=18, pady=(0,8))
        b=ctk.CTkButton(row,text=self.tr("player_add"),command=self._player_add); self.style_button(b,True); b.pack(side="left")
        b=ctk.CTkButton(row,text=self.tr("player_clear"),command=self._player_clear); self.style_button(b); b.pack(side="left", padx=8)

        list_fr=tk.Frame(c,bg=p["panel"]); list_fr.pack(fill="both", expand=True, padx=18, pady=8)
        self.player_list=tk.Listbox(list_fr, bg=p["entry"], fg=p["text"], selectbackground=p["accent"],
                                   font=("Segoe UI",10), activestyle="none", highlightthickness=0, bd=0)
        sb=ttk.Scrollbar(list_fr, orient="vertical", command=self.player_list.yview)
        self.player_list.configure(yscrollcommand=sb.set)
        self.player_list.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.player_list.bind("<Double-Button-1>", lambda e: self._player_play_selected())
        self._player_refresh_list()

        now=tk.Label(c,textvariable=self.player_now,bg=p["panel"],fg=p["accent2"],font=("Segoe UI",10,"bold"))
        now.pack(anchor="w", padx=18, pady=(4,4))

        # Seek bar
        seek_fr=tk.Frame(c,bg=p["panel"]); seek_fr.pack(fill="x", padx=18, pady=(2,4))
        self.player_seek=ttk.Scale(
            seek_fr, from_=0, to=1000, orient="horizontal",
            variable=self.player_pos, command=self._player_on_seek_drag,
        )
        self.player_seek.pack(fill="x", side="left", expand=True)
        self.player_seek.bind("<ButtonPress-1>", lambda e: setattr(self, "player_seeking", True))
        self.player_seek.bind("<ButtonRelease-1>", self._player_on_seek_release)
        tk.Label(seek_fr, textvariable=self.player_time_label, bg=p["panel"], fg=p["muted"],
                 font=("Segoe UI",9), width=14).pack(side="left", padx=(8,0))

        ctrl=tk.Frame(c,bg=p["panel"]); ctrl.pack(fill="x", padx=18, pady=(8,14))
        for txt,cmd in [
            (self.tr("player_prev"), self._player_prev),
            (self.tr("player_play"), self._player_play),
            (self.tr("player_pause"), self._player_pause),
            (self.tr("player_stop"), self._player_stop),
            (self.tr("player_next"), self._player_next),
        ]:
            b=ctk.CTkButton(ctrl,text=txt,command=cmd,width=90)
            self.style_button(b, primary=(txt==self.tr("player_play")))
            b.pack(side="left", padx=(0,6))

        tk.Label(ctrl,text="音量" if self.lang=="ja" else "Vol",bg=p["panel"],fg=p["muted"],font=("Segoe UI",9)).pack(side="left", padx=(16,4))
        ttk.Scale(ctrl, from_=0, to=100, variable=self.player_vol, orient="horizontal", length=120,
                  command=self._player_vol_changed).pack(side="left")
        tk.Checkbutton(
            ctrl,
            text="連続再生" if self.lang=="ja" else "Continuous",
            variable=self.player_continuous,
            bg=p["panel"], fg=p["text"], selectcolor=p["entry"],
            activebackground=p["panel"], activeforeground=p["text"],
            font=("Segoe UI",9),
        ).pack(side="left", padx=(16,0))

    def _player_fmt_time(self, sec):
        try:
            sec=max(0, int(sec))
        except Exception:
            sec=0
        m,s=divmod(sec,60)
        h,m=divmod(m,60)
        if h:
            return f"{h}:{m:02d}:{s:02d}"
        return f"{m}:{s:02d}"

    def _player_probe_duration(self, path):
        ffprobe=tool("ffprobe")
        if not ffprobe:
            return 0.0
        try:
            r=subprocess.run(
                [ffprobe,"-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",path],
                capture_output=True,text=True,encoding="utf-8",errors="replace",
                creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0), timeout=15,
            )
            return float((r.stdout or "").strip() or 0)
        except Exception:
            return 0.0

    def _player_on_seek_drag(self, value=None):
        # Update time label while dragging
        if not self.player_seeking:
            return
        try:
            pos=float(self.player_pos.get()) / 1000.0
        except Exception:
            pos=0.0
        dur=self.player_duration or 0.0
        cur=pos*dur
        self.player_time_label.set(f"{self._player_fmt_time(cur)} / {self._player_fmt_time(dur)}")

    def _player_on_seek_release(self, event=None):
        self.player_seeking=False
        if not self.player_files:
            return
        dur=self.player_duration or 0.0
        if dur <= 0:
            return
        try:
            pos=float(self.player_pos.get()) / 1000.0
        except Exception:
            pos=0.0
        seek_sec=max(0.0, min(dur, pos*dur))
        self.player_seek_offset=seek_sec
        # Restart playback from seek position
        if self.player_proc and self.player_proc.poll() is None:
            self._player_play(start_at=seek_sec)
        elif self.player_paused:
            self._player_play(start_at=seek_sec)

    def _player_tick(self):
        """Update seek bar position while playing."""
        if not getattr(self, "player_proc", None) or self.player_proc.poll() is not None:
            return
        if self.player_seeking:
            self.root.after(300, self._player_tick)
            return
        import time
        dur=self.player_duration or 0.0
        if dur > 0:
            elapsed=time.time() - (self.player_started_at or time.time())
            cur=min(dur, self.player_seek_offset + elapsed)
            try:
                self.player_pos.set(1000.0 * cur / dur)
            except Exception:
                pass
            self.player_time_label.set(f"{self._player_fmt_time(cur)} / {self._player_fmt_time(dur)}")
        self.root.after(400, self._player_tick)

    def _player_refresh_list(self):
        if not hasattr(self, "player_list"):
            return
        self.player_list.delete(0, "end")
        for i,f in enumerate(self.player_files):
            mark="▶ " if i==self.player_index and self.player_proc and self.player_proc.poll() is None else "  "
            self.player_list.insert("end", f"{mark}{os.path.basename(f)}")

    def _player_add(self):
        paths=filedialog.askopenfilenames(
            title=self.tr("player_add"),
            filetypes=[
                ("Media", "*.mp3 *.m4a *.flac *.wav *.ogg *.opus *.aac *.wma *.mp4 *.mkv *.webm *.avi *.mov *.wmv"),
                ("All", "*.*"),
            ],
        )
        for pth in paths:
            if pth and pth not in self.player_files:
                self.player_files.append(pth)
        self._player_refresh_list()

    def _player_clear(self):
        self._player_stop()
        self.player_files=[]
        self.player_index=0
        self.player_now.set("")
        self.player_pos.set(0)
        self.player_time_label.set("0:00 / 0:00")
        self._player_refresh_list()

    def _player_play_selected(self):
        if not hasattr(self, "player_list"):
            return
        sel=self.player_list.curselection()
        if not sel:
            return
        self.player_index=int(sel[0])
        self._player_play()

    def _kill_process(self, proc, timeout=2.0):
        """Terminate a child process reliably on Windows and macOS/Linux."""
        if not proc:
            return
        try:
            if proc.poll() is not None:
                return
        except Exception:
            return
        # Prefer graceful terminate first.
        try:
            proc.terminate()
        except Exception:
            pass
        try:
            proc.wait(timeout=timeout)
            return
        except Exception:
            pass
        # Force-kill the process (and on Windows, its process tree).
        try:
            if sys.platform == "win32":
                try:
                    subprocess.run(
                        ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                        capture_output=True,
                        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                        timeout=5,
                    )
                except Exception:
                    pass
            try:
                proc.kill()
            except Exception:
                pass
            try:
                proc.wait(timeout=2)
            except Exception:
                pass
        except Exception:
            pass

    def _player_stop_proc(self):
        self.player_stop_requested=True
        self.player_gen = getattr(self, "player_gen", 0) + 1
        proc=self.player_proc
        self.player_proc=None
        self.player_paused=False
        self._kill_process(proc, timeout=2.0)

    def _player_vol_changed(self, _value=None):
        """ffplay only reads -volume at launch, so re-apply the slider by
        restarting playback at the current position (debounced)."""
        try:
            if self._vol_after is not None:
                self.root.after_cancel(self._vol_after)
        except Exception:
            pass
        self._vol_after=self.root.after(300,self._player_apply_volume)

    def _player_apply_volume(self):
        self._vol_after=None
        try:
            proc=self.player_proc
            if not (proc and proc.poll() is None) or self.player_paused or not self.player_files:
                return   # next Play uses the new volume automatically
            path=self.player_files[self.player_index]
            if os.path.splitext(path)[1].lower() in (".mp4",".mkv",".webm",".avi",".mov",".wmv",".mpeg",".mpg",".m4v"):
                return   # avoid reopening the video window
            import time
            pos=self.player_seek_offset+(time.time()-(self.player_started_at or time.time()))
            if self.player_duration:
                pos=min(pos,max(0.0,self.player_duration-1.0))
            self._player_play(start_at=max(0.0,pos))
        except Exception:
            pass

    def _player_play(self, start_at=None):
        if not self.player_files:
            return messagebox.showwarning(APP_NAME, "ファイルを追加してください。" if self.lang=="ja" else "Add files first.")
        if self.player_index < 0 or self.player_index >= len(self.player_files):
            self.player_index=0
        path=self.player_files[self.player_index]
        ffplay=tool("ffplay")
        if not ffplay:
            return messagebox.showerror(APP_NAME, "ffplay が見つかりません。BUILD_EXE_ONE_CLICK.bat で再ビルドしてください。" if self.lang=="ja" else "ffplay.exe not found.")

        # Preserve seek if restarting same track
        if start_at is None:
            start_at=0.0
            self.player_seek_offset=0.0
        else:
            self.player_seek_offset=float(start_at)

        self._player_stop_proc()
        # stop_proc sets stop_requested; clear for this new play
        self.player_stop_requested=False

        vol=80
        try:
            vol=int(max(0.0, min(100.0, float(self.player_vol.get()))))
        except Exception:
            vol=80

        # Probe duration for seek bar
        self.player_duration=self._player_probe_duration(path)
        self.player_time_label.set(f"{self._player_fmt_time(self.player_seek_offset)} / {self._player_fmt_time(self.player_duration)}")
        if self.player_duration > 0:
            self.player_pos.set(1000.0 * self.player_seek_offset / self.player_duration)
        else:
            self.player_pos.set(0)

        ext=os.path.splitext(path)[1].lower()
        is_video=ext in (".mp4",".mkv",".webm",".avi",".mov",".wmv",".mpeg",".mpg",".m4v")
        flags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
        cmd=[ffplay, "-autoexit", "-volume", str(vol),
             "-window_title", f"ATRAC Player - {os.path.basename(path)}"]
        if self.player_seek_offset > 0.05:
            cmd += ["-ss", f"{self.player_seek_offset:.3f}"]
        if not is_video:
            # Audio: no window so × cannot steal focus / confuse playlist
            cmd += ["-nodisp", "-vn"]
        cmd.append(path)

        try:
            self.player_gen = getattr(self, "player_gen", 0) + 1
            gen=self.player_gen
            import time
            self.player_started_at=time.time()
            self.player_proc=self._track_proc(subprocess.Popen(cmd, creationflags=flags))
        except Exception as e:
            return messagebox.showerror(APP_NAME, str(e))

        self.player_paused=False
        self.player_now.set(f'{self.tr("player_now")}: {os.path.basename(path)}')
        self._player_refresh_list()
        self.root.after(300, self._player_tick)
        threading.Thread(target=self._player_watch, args=(self.player_proc, gen), daemon=True).start()

    def _player_watch(self, proc, gen):
        if not proc:
            return
        proc.wait()
        if gen != getattr(self, "player_gen", 0):
            return
        if self.player_stop_requested:
            self.player_proc=None
            self.root.after(0, self._player_refresh_list)
            return
        # Natural end of track -> always go next if continuous (default ON)
        self.player_proc=None
        cont=True
        try:
            cont=bool(self.player_continuous.get())
        except Exception:
            cont=True
        if cont and self.player_files:
            if self.player_index < len(self.player_files)-1:
                self.player_index += 1
            else:
                # loop to first
                self.player_index = 0
            self.root.after(0, self._player_play)
        else:
            self.root.after(0, lambda: self.player_now.set(""))
            self.root.after(0, lambda: self.player_pos.set(0))
            self.root.after(0, self._player_refresh_list)

    def _player_pause(self):
        if self.player_proc and self.player_proc.poll() is None:
            # Save approximate position then stop
            import time
            elapsed=time.time() - (self.player_started_at or time.time())
            self.player_seek_offset = min(
                self.player_duration or 1e9,
                self.player_seek_offset + elapsed,
            )
            self._player_stop_proc()
            self.player_paused=True
            name=os.path.basename(self.player_files[self.player_index]) if self.player_files else ""
            self.player_now.set((self.tr("player_pause") + ": " + name))
            self._player_refresh_list()

    def _player_stop(self):
        self._player_stop_proc()
        self.player_seek_offset=0.0
        self.player_pos.set(0)
        self.player_time_label.set(f"0:00 / {self._player_fmt_time(self.player_duration)}")
        self.player_now.set("")
        self._player_refresh_list()

    def _player_prev(self):
        if not self.player_files:
            return
        self.player_index = (self.player_index - 1) % len(self.player_files)
        self._player_play()

    def _player_next(self):
        if not self.player_files:
            return
        self.player_index = (self.player_index + 1) % len(self.player_files)
        self._player_play()

    def page_stream_service(self,service):
        """Dedicated, functional page for Spotify / Apple Music / YouTube Music.

        Service links are kept separately.  For protected subscription streams this page does
        not decrypt or extract the service's DRM media.  Instead it resolves track metadata
        and routes the resolved title to YouTube Music search, or opens the official page.
        """
        self.service_active=service
        self.download_service=service
        p=self.p()
        names={
            "spotify":"Spotifyダウンロード" if self.lang=="ja" else "Spotify Download",
            "apple_music":"Apple Musicダウンロード" if self.lang=="ja" else "Apple Music Download",
            "youtube_music":"YouTube Musicダウンロード" if self.lang=="ja" else "YouTube Music Download",
        }
        service_name=names.get(service,service)
        c=self.card(self.content); c.pack(fill="x")
        tk.Label(c,text=service_name,font=("Segoe UI",18,"bold"),bg=p["panel"],fg=p["text"]).pack(anchor="w",padx=18,pady=(16,4))

        t=tk.Text(c,height=6,relief="flat",bd=0,bg=p["entry"],fg=p["text"],insertbackground=p["text"],font=("Segoe UI",10))
        t.pack(fill="x",padx=18,pady=(6,6))
        if self.service_urls.get(service):
            t.insert("1.0",self.service_urls[service])
        self.service_text_widget=t
        self.online_text=t

        urlrow=tk.Frame(c,bg=p["panel"]); urlrow.pack(fill="x",padx=18,pady=(0,10))
        def sync_text():
            self.service_urls[service]=t.get("1.0","end-1c")
            return self.service_urls[service]
        def first_url():
            raw=sync_text()
            for line in raw.splitlines():
                u=line.strip()
                if u:
                    return u
            return ""
        def clear_links():
            t.delete("1.0","end"); self.service_urls[service]=""
            try:
                self.onprog["value"]=0; self.dl_percent.set("0%"); self.dl_speed.set("-"); self.dl_eta.set("-")
            except Exception:
                pass
        def remove_selected():
            try:
                if t.tag_ranges("sel"):
                    first=t.index("sel.first linestart"); last=t.index("sel.last lineend +1c")
                else:
                    first=t.index("insert linestart"); last=t.index("insert lineend +1c")
                t.delete(first,last); sync_text()
            except Exception:
                pass
        b=ctk.CTkButton(urlrow,text=("選択した項目を削除" if self.lang=="ja" else "Remove selected"),command=remove_selected); self.style_button(b); b.pack(side="left")
        b=ctk.CTkButton(urlrow,text=("すべてクリア" if self.lang=="ja" else "Clear all"),command=clear_links); self.style_button(b); b.pack(side="left",padx=8)

        # Keep the primary action permanently visible beside the URL controls.
        # The lower controls can be clipped on some DPI/window-size combinations.
        dl_label=("ダウンロード開始" if self.lang=="ja" else "Start Download")
        self.downbtn=ctk.CTkButton(
            urlrow, text=dl_label,
            command=lambda:(sync_text(), self.start_download()),
            width=180
        )
        self.style_button(self.downbtn,True)
        self.downbtn.pack(side="right")
        self._add_cancel_button(urlrow)
        try:
            if self.download_active:
                self.downbtn.configure(state="disabled")
        except Exception:
            pass

        # Audio download settings.  Keep the controls separate on every service page,
        # while sharing the user's selected output settings between pages.
        self._svc_load_settings(service,"MP3",("MP3","M4A","FLAC","ADTS (.adts)"))
        row=tk.Frame(c,bg=p["panel"]); row.pack(fill="x",padx=18)
        tk.Label(row,text=self.tr("output"),bg=p["panel"],fg=p["text"],font=("Segoe UI",9,"bold")).pack(side="left")
        ttk.Combobox(row,textvariable=self.online_fmt,state="readonly",values=["MP3","M4A","FLAC","ADTS (.adts)"],width=12).pack(side="left",padx=(6,14))
        tk.Label(row,text=self.tr("audio_quality"),bg=p["panel"],fg=p["text"],font=("Segoe UI",9,"bold")).pack(side="left")
        ttk.Combobox(row,textvariable=self.audio_quality,state="readonly",values=["128 kbps","192 kbps","256 kbps","320 kbps"],width=10).pack(side="left",padx=(6,14))
        tk.Label(row,text=("サンプルレート" if self.lang=="ja" else "Sample Rate"),bg=p["panel"],fg=p["text"],font=("Segoe UI",9,"bold")).pack(side="left")
        ttk.Combobox(row,textvariable=self.online_sample_rate,state="readonly",
                     values=["元のまま","22050 Hz","32000 Hz","44100 Hz","48000 Hz","96000 Hz"],width=12).pack(side="left",padx=(6,14))
        b=ctk.CTkButton(row,text=("ライブラリーを開く" if self.lang=="ja" else "Open Library"),command=self._library_open_root); self.style_button(b); b.pack(side="right")

        self.online_folder_label=ctk.CTkLabel(c,text=self.online_folder.get().strip() or ("保存先: ATRAC Library / Downloads" if self.lang=="ja" else "Saved to: ATRAC Library / Downloads"),anchor="w",text_color=p["muted"])
        self.online_folder_label.pack(fill="x",padx=18,pady=(8,0))

        statrow=tk.Frame(c,bg=p["panel"]); statrow.pack(fill="x",padx=18,pady=(8,4))
        # Reuse the persistent download status variables across page changes.
        tk.Label(statrow,textvariable=self.dl_percent,bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")).pack(side="left")
        tk.Label(statrow,text=self.tr("dl_speed")+":",bg=p["panel"],fg=p["muted"],font=("Segoe UI",9)).pack(side="left",padx=(20,4))
        tk.Label(statrow,textvariable=self.dl_speed,bg=p["panel"],fg=p["text"],font=("Segoe UI",9)).pack(side="left")
        tk.Label(statrow,text=self.tr("dl_eta")+":",bg=p["panel"],fg=p["muted"],font=("Segoe UI",9)).pack(side="left",padx=(20,4))
        tk.Label(statrow,textvariable=self.dl_eta,bg=p["panel"],fg=p["text"],font=("Segoe UI",9)).pack(side="left")
        self.onprog=ttk.Progressbar(c,mode="determinate",maximum=100); self.onprog.pack(fill="x",padx=18,pady=(4,10))

        actionrow=tk.Frame(c,bg=p["panel"]); actionrow.pack(fill="x",padx=18,pady=(0,18))
        def local_convert():
            sync_text(); self.show_page("convert")
        b=ctk.CTkButton(actionrow,text=("手元のファイルを変換" if self.lang=="ja" else "Convert Local Files"),command=local_convert); self.style_button(b); b.pack(side="left")
        try:
            if self.onprog is not None:
                self.onprog["value"]=self._dl_progress_value
        except Exception:
            pass

    def page_music_match(self):
        """Apple / Amazon / LINE / YT Music style: title match from public sources (not DRM rip)."""
        self.download_service="music_match"
        p=self.p()
        c=self.card(self.content); c.pack(fill="x")
        tk.Label(c,text=self.tr("music_match_title"),font=("Segoe UI",16,"bold"),bg=p["panel"],fg=p["text"]).pack(anchor="w",padx=18,pady=(16,4))
        tk.Label(c,text=self.tr("rights"),font=("Segoe UI",9),bg=p["panel"],fg=p["muted"]).pack(anchor="w",padx=18,pady=(0,6))
        tk.Label(c,text=self.tr("music_match_hint"),font=("Segoe UI",9,"bold"),bg=p["panel"],fg=p["muted"],justify="left").pack(anchor="w",padx=18)
        self._svc_load_settings("music_match","MP3",("MP3","M4A","FLAC","ADTS (.adts)"),"320 kbps")
        self.service_active="music_match"
        self.online_text=tk.Text(c,height=6,relief="flat",bd=0,bg=p["entry"],fg=p["text"],insertbackground=p["text"],font=("Segoe UI",10))
        self.online_text.pack(fill="x",padx=18,pady=(8,6))
        self.service_text_widget=self.online_text
        if self.service_urls.get("music_match","").strip():
            self.online_text.insert("1.0",self.service_urls["music_match"])
        row=tk.Frame(c,bg=p["panel"]); row.pack(fill="x", padx=18)
        tk.Label(row,text=self.tr("output"),bg=p["panel"],fg=p["text"],font=("Segoe UI",9,"bold")).pack(side="left")
        ttk.Combobox(row,textvariable=self.online_fmt,state="readonly",
                     values=["MP3","M4A","FLAC","ADTS (.adts)"],width=12).pack(side="left",padx=(6,14))
        tk.Label(row,text=self.tr("audio_quality"),bg=p["panel"],fg=p["text"],font=("Segoe UI",9,"bold")).pack(side="left")
        ttk.Combobox(row,textvariable=self.audio_quality,state="readonly",
                     values=["128 kbps","192 kbps","256 kbps","320 kbps"],width=10).pack(side="left",padx=(6,14))
        b=ctk.CTkButton(row,text=("ライブラリーを開く" if self.lang=="ja" else "Open Library"),command=self._library_open_root); self.style_button(b); b.pack(side="right")
        self.downbtn=ctk.CTkButton(row,text=self.tr("download"),command=self.start_download,width=180); self.style_button(self.downbtn,True); self.downbtn.pack(side="right",padx=(0,8))
        self._add_cancel_button(row)
        try:
            if self.download_active:
                self.downbtn.configure(state="disabled")
        except Exception:
            pass
        self.online_folder_label=ctk.CTkLabel(c, text=self.online_folder.get().strip() or ("保存先: ATRAC Library / Downloads" if self.lang=="ja" else "Saved to: ATRAC Library / Downloads"), anchor="w", text_color=p["muted"])
        self.online_folder_label.pack(fill="x", padx=18, pady=(8,0))
        statrow=tk.Frame(c,bg=p["panel"]); statrow.pack(fill="x", padx=18, pady=(8,4))
        # Reuse the persistent download status variables across page changes.
        tk.Label(statrow,textvariable=self.dl_percent,bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")).pack(side="left")
        self.onprog=ttk.Progressbar(c,mode="determinate",maximum=100); self.onprog.pack(fill="x", padx=18, pady=(4,14))
        try:
            if self.onprog is not None:
                self.onprog["value"]=self._dl_progress_value
        except Exception:
            pass
        tk.Frame(c,bg=p["panel"],height=12).pack()

    def page_youtube(self):
        return self._page_download_service("youtube")

    def page_tiktok(self):
        return self._page_download_service("tiktok")

    def _page_download_service(self,service):
        self.download_service=service
        p=self.p()
        c=self.card(self.content);c.pack(fill="x")
        title_key = {"youtube":"youtube_title","tiktok":"tiktok_title"}.get(service,"youtube_title")
        hint_key = {"youtube":"youtube_hint","tiktok":"tiktok_hint"}.get(service,"youtube_hint")
        tk.Label(c,text=self.tr(title_key),font=("Segoe UI",16,"bold"),bg=p["panel"],fg=p["text"]).pack(anchor="w",padx=18,pady=(16,4))
        tk.Label(c,text=self.tr("rights"),font=("Segoe UI",9),bg=p["panel"],fg=p["muted"]).pack(anchor="w",padx=18,pady=(0,10))

        tk.Label(c,text=self.tr(hint_key),font=("Segoe UI",9,"bold"),bg=p["panel"],fg=p["muted"],justify="left").pack(anchor="w",padx=18)
        self.online_text=tk.Text(c,height=5,relief="flat",bd=0,bg=p["entry"],fg=p["text"],insertbackground=p["text"],font=("Segoe UI",10))
        self.online_text.pack(fill="x",padx=18,pady=(5,6))
        self.service_active=service
        self.service_text_widget=self.online_text
        self._svc_load_settings(service,"MP4",("MP4","MP3","M4A","FLAC","ADTS (.adts)"))
        if self.service_urls.get(service,"").strip():
            self.online_text.insert("1.0",self.service_urls[service])

        url_actions=tk.Frame(c,bg=p["panel"]);url_actions.pack(fill="x",padx=18,pady=(0,10))
        def remove_selected_url():
            try:
                if self.online_text.tag_ranges("sel"):
                    first=self.online_text.index("sel.first linestart")
                    last=self.online_text.index("sel.last lineend +1c")
                else:
                    first=self.online_text.index("insert linestart")
                    last=self.online_text.index("insert lineend +1c")
                self.online_text.delete(first,last)
            except Exception:
                pass
        def clear_all_urls():
            self.online_text.delete("1.0","end")
            self.service_urls[service]=""
            try:
                self.onprog["value"]=0
                self.dl_percent.set("0%")
                self.dl_speed.set("-")
                self.dl_eta.set("-")
            except Exception:
                pass
        b=ctk.CTkButton(url_actions,text=self.tr("remove_selected_url"),command=remove_selected_url);self.style_button(b);b.pack(side="left")
        b=ctk.CTkButton(url_actions,text=self.tr("clear_all_urls"),command=clear_all_urls);self.style_button(b);b.pack(side="left",padx=8)

        # Keep the primary action visible near the URL box instead of placing it
        # at the very bottom of the page where smaller windows can clip it.
        self.downbtn=ctk.CTkButton(
            url_actions,
            text=self.tr("download"),
            command=self.start_download,
            width=170
        )
        self.style_button(self.downbtn,True)
        self.downbtn.pack(side="right")
        self._add_cancel_button(url_actions)
        try:
            if self.download_active:
                self.downbtn.configure(state="disabled")
        except Exception:
            pass

        row=tk.Frame(c,bg=p["panel"]);row.pack(fill="x",padx=18)
        tk.Label(row,text=self.tr("output"),bg=p["panel"],fg=p["text"],font=("Segoe UI",9,"bold")).pack(side="left")
        ttk.Combobox(row,textvariable=self.online_fmt,state="readonly",
                     values=["MP4","MP3","M4A","FLAC","ADTS (.adts)"],width=12).pack(side="left",padx=(6,14))

        tk.Label(row,text=self.tr("video_quality"),bg=p["panel"],fg=p["text"],font=("Segoe UI",9,"bold")).pack(side="left")
        ttk.Combobox(row,textvariable=self.video_quality,state="readonly",
                     values=["Best","2160p","1440p","1080p","720p","480p","360p"],width=9).pack(side="left",padx=(6,14))

        tk.Label(row,text=self.tr("audio_quality"),bg=p["panel"],fg=p["text"],font=("Segoe UI",9,"bold")).pack(side="left")
        ttk.Combobox(row,textvariable=self.audio_quality,state="readonly",
                     values=["128 kbps","192 kbps","256 kbps","320 kbps"],width=10).pack(side="left",padx=(6,14))

        b=ctk.CTkButton(row,text=("ライブラリーを開く" if self.lang=="ja" else "Open Library"),command=self._library_open_root);self.style_button(b);b.pack(side="right")

        self.online_folder_label=ctk.CTkLabel(
            c,
            text=self.online_folder.get().strip() or ("保存先: ATRAC Library / Downloads" if self.lang=="ja" else "Saved to: ATRAC Library / Downloads"),
            anchor="w",
            text_color=p["muted"]
        )
        self.online_folder_label.pack(fill="x",padx=18,pady=(8,0))

        statrow=tk.Frame(c,bg=p["panel"]);statrow.pack(fill="x",padx=18,pady=(8,4))
        # Reuse the persistent download status variables across page changes.
        tk.Label(statrow,textvariable=self.dl_percent,bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")).pack(side="left")
        tk.Label(statrow,text=self.tr("dl_speed")+":",bg=p["panel"],fg=p["muted"],font=("Segoe UI",9)).pack(side="left",padx=(20,4))
        tk.Label(statrow,textvariable=self.dl_speed,bg=p["panel"],fg=p["text"],font=("Segoe UI",9)).pack(side="left")
        tk.Label(statrow,text=self.tr("dl_eta")+":",bg=p["panel"],fg=p["muted"],font=("Segoe UI",9)).pack(side="left",padx=(20,4))
        tk.Label(statrow,textvariable=self.dl_eta,bg=p["panel"],fg=p["text"],font=("Segoe UI",9)).pack(side="left")
        self.onprog=ttk.Progressbar(c,mode="determinate",maximum=100);self.onprog.pack(fill="x",padx=18,pady=(4,18))
        try:
            if self.onprog is not None:
                self.onprog["value"]=self._dl_progress_value
            if self.download_active:
                self.downbtn.configure(state="disabled")
        except Exception:
            pass

    def pick_online(self):
        p=self._library_download_dir()
        self.online_folder.set(p)
        if hasattr(self,"online_folder_label"):
            self.online_folder_label.configure(text=p)
        self._library_open_root()

    def _youtube_music_search_url(self, query):
        q=str(query or "").strip()
        if not q:
            raise RuntimeError("検索する曲名がありません。" if self.lang=="ja" else "No track title to search.")
        return "https://music.youtube.com/search?q="+urllib.parse.quote_plus(q)

    def _youtube_music_resolve_watch_url(self, query):
        """Resolve a title/artist query to an actual YouTube Music watch URL.
        Uses ytmusicapi only for search/metadata. The resulting music.youtube.com URL is
        then handled by the existing yt-dlp download worker.
        """
        q=str(query or "").strip()
        if not q:
            raise RuntimeError("検索する曲名がありません。" if self.lang=="ja" else "No track title to search.")
        try:
            from ytmusicapi import YTMusic
        except Exception as e:
            raise RuntimeError(
                ("YouTube Music検索機能がありません。One Click Builderで再ビルドしてください。\n" if self.lang=="ja" else
                 "YouTube Music search support is missing. Rebuild with One Click Builder.\n") + str(e)
            )
        ytm=YTMusic()
        results=[]
        try:
            results=ytm.search(q, filter="songs", limit=5) or []
        except Exception:
            results=[]
        if not results:
            try:
                results=ytm.search(q, filter="videos", limit=5) or []
            except Exception:
                results=[]
        for r in results:
            vid=(r or {}).get("videoId")
            if vid:
                return "https://music.youtube.com/watch?v="+str(vid)
        raise RuntimeError(
            f"YouTube Musicで見つかりませんでした: {q}" if self.lang=="ja" else f"Not found on YouTube Music: {q}"
        )

    def _route_service_to_youtube_music(self, service, urls):
        """Resolve service metadata to YouTube Music search URLs without opening any browser."""
        queries=[]
        direct=[]
        if service=="spotify":
            prepared=self._spotify_prepare_urls(urls)
            metas=getattr(self,"_dl_meta_list",[]) or []
            for i,u in enumerate(prepared):
                m=metas[i] if i < len(metas) else None
                if m and m.get("query"):
                    queries.append(m.get("query"))
                elif isinstance(u,str) and u.startswith("ytsearch"):
                    queries.append(u.split(":",1)[-1])
        else:
            prepared=self._music_match_prepare_urls(urls)
            metas=getattr(self,"_dl_meta_list",[]) or []
            for i,u in enumerate(prepared):
                m=metas[i] if i < len(metas) else None
                if m and m.get("query"):
                    queries.append(m.get("query"))
                elif isinstance(u,str) and u.startswith("ytsearch"):
                    queries.append(u.split(":",1)[-1])
                elif isinstance(u,str) and "music.youtube.com/" in u:
                    direct.append(u)
        watch_urls=list(direct)
        for q in queries:
            watch_urls.append(self._youtube_music_resolve_watch_url(q))
        if not watch_urls:
            return []
        return watch_urls

    def start_download(self):
        try:
            if self.download_active:
                return messagebox.showinfo(APP_NAME, "ダウンロードはバックグラウンドで続行中です。" if self.lang=="ja" else "A download is already running in the background.")
            raw=self.online_text.get("1.0","end").strip() if getattr(self,"online_text",None) is not None else self.online_url.get().strip()
            urls=[u.strip() for u in raw.splitlines() if u.strip()]

            if not urls:
                return messagebox.showwarning(APP_NAME,self.tr("need_url"))

            service=getattr(self,"download_service","youtube")
            self._dl_meta_list=None   # never reuse metadata from a previous service's run
            if service=="youtube":
                bad=[u for u in urls if not (
                    "youtube.com/" in u.lower() or
                    "youtu.be/" in u.lower() or
                    "music.youtube.com/" in u.lower()
                )]
                if bad:
                    return messagebox.showerror(
                        APP_NAME,
                        "YouTube のURLを入力してください。" if self.lang=="ja" else "Please enter YouTube URLs."
                    )
            elif service=="tiktok":
                bad=[u for u in urls if not (
                    "tiktok.com/" in u.lower() or
                    "vm.tiktok.com/" in u.lower() or
                    "vt.tiktok.com/" in u.lower()
                )]
                if bad:
                    return messagebox.showerror(
                        APP_NAME,
                        "TikTokのURLを入力してください。" if self.lang=="ja" else "Please enter TikTok URLs."
                    )
            elif service in ("spotify","apple_music","amazon_music"):
                # Metadata lookup and YouTube Music matching can take several seconds.
                # Keep it off the Tk thread; download_batch_worker resolves it.
                self._dl_meta_list=None
            elif service=="youtube_music":
                bad=[u for u in urls if not (
                    "music.youtube.com/" in u.lower() or
                    "youtube.com/" in u.lower() or
                    "youtu.be/" in u.lower()
                )]
                if bad:
                    return messagebox.showerror(
                        APP_NAME,
                        "YouTube Music / YouTube のURLを入力してください。" if self.lang=="ja" else "Please enter YouTube Music / YouTube URLs."
                    )
                self._dl_meta_list=None
            elif service=="music_match":
                # Resolve links/titles in the background worker.
                self._dl_meta_list=None
            else:
                self._dl_meta_list=None

            # TuneFab-style library behaviour: downloads go straight into the app library.
            # No save-location dialog is required for every download.
            folder=self._library_download_dir()
            self.online_folder.set(folder)
            if hasattr(self,"online_folder_label"):
                try:self.online_folder_label.configure(text=folder)
                except Exception:pass

            self.online_url.set("\n".join(urls))
            self._dl_submitted=list(urls)      # remembered so they can be cleared after success
            self._dl_service_key=service
            self.dl_batch_total=len(urls)
            self.dl_batch_index=1

            # Give immediate visual feedback before starting the worker thread.
            try:
                self._cancel_work.clear()
            except Exception:
                pass
            self._app_closing=False
            self._user_cancelled=False
            self._dl_started_at=__import__("time").time()
            self._reset_dl_ui()
            self.dl_percent.set(
                "開始中..." if self.lang=="ja" else "Starting..."
            )
            self.download_active=True
            self._set_cancel_state(True)
            try:
                if self.downbtn is not None and self.downbtn.winfo_exists():
                    self.downbtn.configure(state="disabled")
            except Exception:
                pass
            meta_list=getattr(self,"_dl_meta_list",None)
            sr_value=None
            if service in ("spotify","apple_music","youtube_music"):
                raw_sr=self.online_sample_rate.get().strip()
                if raw_sr not in ("","元のまま","Original"):
                    m=re.search(r"(\d+)",raw_sr)
                    sr_value=m.group(1) if m else None
            threading.Thread(
                target=self.download_batch_worker,
                args=(
                    urls,
                    folder,
                    self.online_fmt.get(),
                    self.video_quality.get(),
                    self.audio_quality.get(),
                    meta_list,
                    sr_value,
                    service,
                ),
                daemon=True
            ).start()

        except Exception as e:
            self.download_active=False
            try:
                if self.downbtn is not None and self.downbtn.winfo_exists():
                    self.downbtn.configure(state="normal")
            except Exception:
                pass
            messagebox.showerror(
                APP_NAME,
                ("ダウンロード開始エラー:\n" if self.lang=="ja" else "Download start error:\n") + str(e)
            )

    def _format_bytes(self,n):
        if not n:return "-"
        if isinstance(n,str):
            t=n.strip()
            return t if t and t not in ("NA","N/A","Unknown") else "-"
        units=["B/s","KB/s","MB/s","GB/s"]
        v=float(n);i=0
        while v>=1024 and i<len(units)-1:
            v/=1024;i+=1
        return f"{v:.1f} {units[i]}"

    def _format_eta(self,s):
        if s is None:return "-"
        if isinstance(s,str):
            t=s.strip()
            return t if t and t not in ("NA","N/A","Unknown") else "-"
        try:
            s=int(s)
            m,sec=divmod(s,60);h,m=divmod(m,60)
            return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"
        except:return "-"

    def _progress_hook(self,d):
        if d.get("status")=="downloading":
            total=d.get("total_bytes") or d.get("total_bytes_estimate")
            done=d.get("downloaded_bytes") or 0
            pct=(done/total*100) if total else 0
            speed=d.get("speed")
            eta=d.get("eta")
            self._post_dl_ui("progress",pct,speed,eta)
        elif d.get("status")=="finished":
            self._post_dl_ui("progress",100,None,0)

    def _update_dl_ui(self,pct,speed,eta):
        try:
            self._dl_progress_value=max(0.0,min(100.0,float(pct)))
        except Exception:
            self._dl_progress_value=0.0
        try:
            if self.onprog is not None and self.onprog.winfo_exists():
                self.onprog["value"]=self._dl_progress_value
        except Exception:
            pass
        prefix=(f"{self.dl_batch_index}/{self.dl_batch_total}  " if self.dl_batch_total>1 else "")
        try:self.dl_percent.set(prefix+f"{self._dl_progress_value:.1f}%")
        except Exception:pass
        try:self.dl_speed.set(self._format_bytes(speed))
        except Exception:pass
        try:self.dl_eta.set(self._format_eta(eta))
        except Exception:pass

    def download_batch_worker(self,urls,folder,fmt,video_quality,audio_quality,meta_list=None,sample_rate=None,service=None):
        try:
            service=service or getattr(self,"download_service","youtube")
            if service in ("youtube","tiktok"):
                meta_list=None
            # All network-heavy metadata resolution happens here, never on Tk's UI thread.
            if service in ("spotify","apple_music","amazon_music"):
                self._post_dl_ui("status", "曲情報を取得中..." if self.lang=="ja" else "Resolving track information...")
                urls=self._route_service_to_youtube_music(service, list(urls))
                meta_list=getattr(self,"_dl_meta_list",None)
                if self._is_work_cancelled():
                    raise RuntimeError("ダウンロードをキャンセルしました。" if self.lang=="ja" else "Download cancelled.")
                if not urls:
                    raise RuntimeError("YouTube Musicで曲を見つけられませんでした。" if self.lang=="ja" else "Could not find the track on YouTube Music.")
            elif service=="music_match":
                self._post_dl_ui("status", "曲情報を取得中..." if self.lang=="ja" else "Resolving track information...")
                urls=self._music_match_prepare_urls(list(urls))
                meta_list=getattr(self,"_dl_meta_list",None)
                if self._is_work_cancelled():
                    raise RuntimeError("ダウンロードをキャンセルしました。" if self.lang=="ja" else "Download cancelled.")
                if not urls:
                    raise RuntimeError("ダウンロード対象を見つけられませんでした。" if self.lang=="ja" else "No downloadable item was found.")

            self.dl_batch_total=len(urls)
            for i,url in enumerate(urls,1):
                if self._is_work_cancelled():
                    raise RuntimeError("ダウンロードをキャンセルしました。" if self.lang=="ja" else "Download cancelled.")
                self.dl_batch_index=i
                self._post_dl_ui("reset")
                meta=None
                if meta_list and i-1 < len(meta_list):
                    meta=meta_list[i-1]
                self.download_worker(url,folder,fmt,video_quality,audio_quality,meta=meta,sample_rate=sample_rate)
            if self._is_work_cancelled():
                raise RuntimeError("ダウンロードをキャンセルしました。" if self.lang=="ja" else "Download cancelled.")
            self._post_dl_ui("success")
        except Exception as e:
            if self._is_work_cancelled():
                # Quiet exit while the window is closing — avoid a dialog on a dead UI.
                try:
                    if not getattr(self, "_app_closing", False):
                        self._post_dl_ui("error", str(e))
                except Exception:
                    pass
            else:
                self._post_dl_ui("error",str(e))

    def _video_format_string(self,quality):
        # YouTube commonly limits single-file MP4 streams to a lower resolution.
        # Prefer the best separate video+audio streams first so 1080p/1440p/2160p
        # selections can actually use the requested resolution, then merge with ffmpeg.
        if quality=="Best":
            return "bv*[ext=mp4]+ba[ext=m4a]/bv*+ba/best"
        try:
            h=int(quality.lower().replace("p",""))
        except:
            h=1080
        return (f"bv*[ext=mp4][height<={h}]+ba[ext=m4a]/"
                f"bv*[height<={h}]+ba/"
                f"b[height<={h}]")

    def _spotify_http_get(self,url,timeout=20):
        """HTTP GET that works better inside frozen EXE (explicit SSL context)."""
        ctx=ssl.create_default_context()
        try:
            import certifi
            ctx=ssl.create_default_context(cafile=certifi.where())
        except Exception:
            pass
        # Some Windows EXEs have broken default CA store; allow fallback.
        try:
            req=urllib.request.Request(
                url,
                headers={
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36",
                    "Accept":"application/json,text/html,*/*",
                    "Accept-Language":"en-US,en;q=0.9,ja;q=0.8",
                },
            )
            with urllib.request.urlopen(req,timeout=timeout,context=ctx) as resp:
                return resp.read().decode("utf-8","replace")
        except Exception:
            ctx2=ssl._create_unverified_context()
            req=urllib.request.Request(
                url,
                headers={
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36",
                    "Accept":"application/json,text/html,*/*",
                },
            )
            with urllib.request.urlopen(req,timeout=timeout,context=ctx2) as resp:
                return resp.read().decode("utf-8","replace")

    def _http_get_with_final_url(self,url,timeout=20):
        """HTTP GET returning (html, final_url) after redirects. Useful for short music share links."""
        ctx=ssl.create_default_context()
        try:
            import certifi
            ctx=ssl.create_default_context(cafile=certifi.where())
        except Exception:
            pass
        headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
            "Accept-Language":"ja,en-US;q=0.9,en;q=0.8",
        }
        last=None
        for context in (ctx, ssl._create_unverified_context()):
            try:
                req=urllib.request.Request(url,headers=headers)
                with urllib.request.urlopen(req,timeout=timeout,context=context) as resp:
                    return resp.read().decode("utf-8","replace"), resp.geturl()
            except Exception as e:
                last=e
        raise last or RuntimeError("HTTP request failed")

    def _spotify_normalize_url(self,spotify_url):
        u=spotify_url.strip()
        u=re.sub(r"https?://open\.spotify\.com/intl-[a-z]{2}/",
                 "https://open.spotify.com/",u,flags=re.I)
        u=u.split("?")[0].split("#")[0]
        return u

    def _spotify_parse_id(self,spotify_url,kinds=("track","album","playlist","episode","show")):
        u=self._spotify_normalize_url(spotify_url)
        for kind in kinds:
            m=re.search(rf"(?:/{kind}/|spotify:{kind}:)([a-zA-Z0-9]{{22}})",u,re.I)
            if m:
                return kind.lower(), m.group(1)
        return None, None

    def _spotify_embed_entity(self,kind,sid):
        """Fetch album/playlist/track metadata from public embed page (no API key)."""
        html=self._spotify_http_get(f"https://open.spotify.com/embed/{kind}/{sid}")
        m=re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',html,re.S)
        if not m:
            return None
        data=json.loads(m.group(1))
        try:
            return data["props"]["pageProps"]["state"]["data"]["entity"]
        except Exception:
            return None

    def _spotify_cover_url(self,entity):
        """Pick the largest cover image from embed visualIdentity."""
        try:
            images=((entity or {}).get("visualIdentity") or {}).get("image") or []
            if not images:
                return None
            best=max(images, key=lambda im: int(im.get("maxWidth") or im.get("maxHeight") or 0))
            return best.get("url")
        except Exception:
            return None

    def _spotify_entries_from_entity(self,entity):
        """Return list of dicts: index, title, artist, query, cover_url."""
        if not entity:
            return []
        cover=self._spotify_cover_url(entity)
        album=(entity.get("name") or entity.get("title") or "").strip()
        et=str(entity.get("type") or "").lower()
        out=[]
        if et=="track":
            title=(entity.get("title") or entity.get("name") or "").strip()
            artist=(entity.get("subtitle") or "").strip()
            if not artist:
                arts=entity.get("artists") or []
                names=[]
                for a in arts:
                    if isinstance(a, dict) and a.get("name"):
                        names.append(str(a.get("name")).strip())
                    elif isinstance(a, str) and a.strip():
                        names.append(a.strip())
                artist=", ".join(names)
            if title:
                out.append({
                    "index":1,
                    "title":title,
                    "artist":artist,
                    "album":album,
                    "query":f"{title} {artist}".strip(),
                    "cover_url":cover,
                })
            return out
        for i,t in enumerate(entity.get("trackList") or [], 1):
            title=(t.get("title") or t.get("name") or "").strip()
            artist=(t.get("subtitle") or "").strip()
            if not title:
                continue
            out.append({
                "index":i,
                "title":title,
                "artist":artist,
                "album":album,
                "query":f"{title} {artist}".strip(),
                "cover_url":cover,
            })
        return out

    def _spotify_oembed_title(self,spotify_url):
        """Resolve a single track title (+ artist when possible)."""
        u=self._spotify_normalize_url(spotify_url)
        # 1) Embed entity (best: title + artist)
        kind,sid=self._spotify_parse_id(u,("track",))
        if sid:
            try:
                ent=self._spotify_embed_entity("track",sid)
                qs=self._spotify_entries_from_entity(ent)
                if qs:
                    return qs[0].get("query") or qs[0].get("title")
            except Exception:
                pass
        # 2) oEmbed
        try:
            q=urllib.parse.quote(u,safe="")
            api=f"https://open.spotify.com/oembed?url={q}"
            data=json.loads(self._spotify_http_get(api))
            title=(data.get("title") or "").strip()
            if title:
                return title
        except Exception:
            pass
        # 3) crude scrape
        if sid:
            try:
                html=self._spotify_http_get(f"https://open.spotify.com/embed/track/{sid}")
                names=re.findall(r'"name":"([^"\\]{1,120})"',html)
                names=[n for n in names if n and n.lower() not in ("spotify","embed")]
                if names:
                    return f"{names[0]} {names[1]}".strip() if len(names)>=2 else names[0]
            except Exception:
                pass
        return None

    def _spotify_ask_manual_title(self,spotify_url):
        prompt=("曲名を自動取得できませんでした。\n"
                "検索用の曲名（できれば『曲名 アーティスト』）を入力してください。"
                if self.lang=="ja" else
                "Could not auto-resolve the track title.\n"
                "Enter a search title (preferably 'Song Artist').")
        return self._ask_ui_string(APP_NAME,prompt)

    def _spotify_prepare_urls(self,urls):
        """
        Main-thread only.
        Convert Spotify links / plain titles into ytsearch1 queries.
        Also fills self._dl_meta_list for track numbers + cover art.
        """
        out=[]
        meta_list=[]
        for raw in urls:
            url=raw.strip()
            if not url:
                continue
            low=url.lower()
            looks_like_url=("http://" in low or "https://" in low or low.startswith("spotify:"))

            if not looks_like_url:
                out.append(f"ytsearch1:{url}")
                meta_list.append({
                    "index": len(meta_list)+1,
                    "title": url,
                    "artist": "",
                    "album": "",
                    "query": url,
                    "cover_url": None,
                })
                continue

            kind,sid=self._spotify_parse_id(url)
            if kind in ("episode","show"):
                out.append(self._spotify_normalize_url(url))
                meta_list.append(None)
                continue

            if kind in ("album","playlist") and sid:
                self._post_dl_ui(
                    "status",
                    ("アルバム取得中..." if kind=="album" else "プレイリスト取得中...")
                    if self.lang=="ja" else
                    ("Fetching album..." if kind=="album" else "Fetching playlist...")
                )
                try:
                    ent=self._spotify_embed_entity(kind,sid)
                    entries=self._spotify_entries_from_entity(ent)
                except Exception as e:
                    raise RuntimeError(
                        f"Spotifyの{kind}情報を取得できませんでした。\n{e}\n"
                        "インターネット接続を確認するか、曲名を直接入力してください。"
                        if self.lang=="ja" else
                        f"Could not fetch Spotify {kind}.\n{e}"
                    )
                if not entries:
                    raise RuntimeError(
                        "アルバム/プレイリストから曲一覧を取得できませんでした。\n"
                        "非公開の可能性、または地域制限の可能性があります。"
                        if self.lang=="ja" else
                        "Could not read track list (private or region-locked?)."
                    )
                name=(ent or {}).get("name") or (ent or {}).get("title") or kind
                if self.lang=="ja":
                    msg="「%s」\n%d 曲をダウンロードします。よろしいですか？" % (name, len(entries))
                else:
                    msg='"%s"\nDownload %d tracks?' % (name, len(entries))
                if not self._ask_ui_yesno(APP_NAME,msg):
                    continue
                for e in entries:
                    out.append(f"ytsearch1:{e['query']}")
                    meta_list.append(e)
                continue

            if kind=="track" and sid:
                self._post_dl_ui(
                    "status",
                    "Spotify曲名を取得中..." if self.lang=="ja" else "Resolving Spotify title..."
                )
                entry=None
                try:
                    ent=self._spotify_embed_entity("track",sid)
                    entries=self._spotify_entries_from_entity(ent)
                    if entries:
                        entry=entries[0]
                except Exception:
                    entry=None
                if not entry:
                    title=None
                    try:
                        title=self._spotify_oembed_title(url)
                    except Exception:
                        title=None
                    if not title:
                        title=self._spotify_ask_manual_title(url)
                    if not title or not str(title).strip():
                        raise RuntimeError(
                            "曲名を自動取得できませんでした。\n曲名を直接入力してください。"
                            if self.lang=="ja" else
                            "Could not resolve title. Type the song name."
                        )
                    entry={
                        "index":1,
                        "title":str(title).strip(),
                        "artist":"",
                        "album":"",
                        "query":str(title).strip(),
                        "cover_url":None,
                    }
                out.append(f"ytsearch1:{entry['query']}")
                meta_list.append(entry)
                continue

            raise RuntimeError(
                "対応していないSpotifyリンクです。\n"
                "曲 / アルバム / プレイリストのリンク、または曲名を入力してください。\n"
                f"入力: {url[:80]}"
                if self.lang=="ja" else
                f"Unsupported Spotify link.\nGot: {url[:80]}"
            )

        self._dl_meta_list=meta_list
        return out


    def _json_http_get(self,url,timeout=20):
        txt=self._spotify_http_get(url,timeout=timeout)
        return json.loads(txt)

    def _apple_music_entries(self,url):
        """Resolve Apple Music track/album links through Apple's public iTunes lookup metadata."""
        u=urllib.parse.urlparse(url)
        qs=urllib.parse.parse_qs(u.query)
        track_id=(qs.get("i") or [None])[0]
        m=re.search(r"/album/[^/]+/(\d+)",u.path,re.I)
        album_id=m.group(1) if m else None
        lookup_id=track_id or album_id
        if not lookup_id:
            return []
        api=f"https://itunes.apple.com/lookup?id={urllib.parse.quote(str(lookup_id))}&entity=song&limit=200"
        data=self._json_http_get(api,timeout=20)
        rows=data.get("results") or []
        # For a track URL, keep only that track. For an album URL, return every song.
        if track_id:
            rows=[r for r in rows if str(r.get("trackId") or "")==str(track_id)] or rows[:1]
        else:
            rows=[r for r in rows if r.get("wrapperType")=="track"]
        out=[]
        for i,r in enumerate(rows,1):
            title=str(r.get("trackName") or "").strip()
            artist=str(r.get("artistName") or "").strip()
            album=str(r.get("collectionName") or "").strip()
            if not title:
                continue
            cover=r.get("artworkUrl100")
            if cover:
                cover=re.sub(r"/\d+x\d+bb\.","/600x600bb.",str(cover))
            out.append({
                "index": int(r.get("trackNumber") or i),
                "title": title,
                "artist": artist,
                "album": album,
                "query": f"{title} {artist}".strip(),
                "cover_url": cover,
            })
        return out

    def _html_meta_content(self,html,key,attr="property"):
        # Handles either property=og:* or name=* meta tags, regardless of attribute order.
        pat1=rf'<meta[^>]+{attr}=["\']{re.escape(key)}["\'][^>]+content=["\']([^"\']+)'
        pat2=rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+{attr}=["\']{re.escape(key)}["\']'
        m=re.search(pat1,html,re.I) or re.search(pat2,html,re.I)
        return html_unescape(m.group(1)).strip() if m else ""

    def _amazon_music_entry(self,url):
        """Resolve Amazon Music share/player URLs and extract track title/artist."""
        original=url.strip()

        def _clean(v):
            if not v:
                return ""
            v=html_unescape(str(v)).strip()
            # Decode common JSON escapes without corrupting normal Unicode.
            try:
                if v.startswith('"') and v.endswith('"'):
                    v=json.loads(v)
            except Exception:
                pass
            v=v.replace('\\/','/').replace('\\u0026','&')
            return re.sub(r"\s+"," ",v).strip()

        def _usable(v):
            v=_clean(v)
            if not v:
                return ""
            low=v.lower().strip()
            generic=("amazon music unlimited","amazon music: songs","amazon music","amazon.com","amazon.co.jp")
            if low in generic or low.startswith("amazon music |"):
                return ""
            return v

        # First resolve shortened share URLs (amzn.to / amzn.asia / amazon share URLs).
        resolved=original
        first_html=""
        try:
            first_html,resolved=self._http_get_with_final_url(original,timeout=25)
        except Exception:
            pass

        # Build canonical public album/player URLs from BOTH original and redirect target.
        candidates=[]
        if first_html:
            candidates.append((resolved,first_html))
        for base in (resolved,original):
            try:
                u=urllib.parse.urlparse(base)
                path=u.path or ""
                qs=urllib.parse.parse_qs(u.query)
                album_asin=""
                track_asin=(qs.get("trackAsin") or qs.get("trackasin") or [""])[0].upper()
                m=re.search(r"/(?:albums|music/player/albums)/(B[0-9A-Z]{9})",path,re.I)
                if m: album_asin=m.group(1).upper()
                # Some links carry the track directly in the path.
                tm=re.search(r"/(?:tracks|music/player/tracks)/(B[0-9A-Z]{9})",path,re.I)
                if tm and not track_asin: track_asin=tm.group(1).upper()
                territory=(qs.get("musicTerritory") or qs.get("musicterritory") or [""])[0]
                if album_asin:
                    q={}
                    if track_asin: q["trackAsin"]=track_asin
                    if territory: q["musicTerritory"]=territory
                    qtxt=urllib.parse.urlencode(q)
                    for host in ("music.amazon.com","music.amazon.co.jp"):
                        candidates.append((f"https://{host}/albums/{album_asin}"+("?"+qtxt if qtxt else ""),None))
                candidates.append((base,None))
            except Exception:
                candidates.append((base,None))

        # De-duplicate URLs.
        uniq=[]; seen=set()
        for u,h in candidates:
            if u and u not in seen:
                seen.add(u); uniq.append((u,h))

        last_error=None
        for candidate,prefetched in uniq:
            try:
                if prefetched is not None:
                    html=prefetched
                    final_url=candidate
                else:
                    html,final_url=self._http_get_with_final_url(candidate,timeout=25)
            except Exception as e:
                last_error=e
                continue

            title=_usable(self._html_meta_content(html,"og:title") or self._html_meta_content(html,"twitter:title","name"))
            desc=_clean(self._html_meta_content(html,"og:description") or self._html_meta_content(html,"description","name"))
            cover=self._html_meta_content(html,"og:image")
            artist=""; album=""

            # Normal HTML title.
            if not title:
                tm=re.search(r"<title[^>]*>(.*?)</title>",html,re.I|re.S)
                if tm:
                    title=_usable(re.sub(r"<[^>]+>","",tm.group(1)))

            # JSON-LD metadata.
            for raw in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',html,re.I|re.S):
                try:
                    obj=json.loads(html_unescape(raw.strip()))
                except Exception:
                    continue
                stack=obj if isinstance(obj,list) else [obj]
                while stack:
                    o=stack.pop(0)
                    if isinstance(o,list):
                        stack.extend(o); continue
                    if not isinstance(o,dict):
                        continue
                    typ=str(o.get("@type") or "")
                    if typ in ("MusicRecording","MusicAlbum","MusicGroup"):
                        if typ=="MusicRecording": title=_usable(o.get("name")) or title
                        by=o.get("byArtist") or o.get("artist")
                        if isinstance(by,dict): artist=_clean(by.get("name")) or artist
                        elif isinstance(by,list):
                            names=[_clean(x.get("name")) for x in by if isinstance(x,dict) and x.get("name")]
                            if names: artist=", ".join(names)
                        alb=o.get("inAlbum")
                        if isinstance(alb,dict): album=_clean(alb.get("name")) or album
                    for v in o.values():
                        if isinstance(v,(dict,list)): stack.append(v)

            # Determine trackAsin from the final redirected URL too, then inspect nearby JSON.
            track_asin=""
            for uu in (final_url,candidate,resolved,original):
                try:
                    pu=urllib.parse.urlparse(uu)
                    pqs=urllib.parse.parse_qs(pu.query)
                    track_asin=(pqs.get("trackAsin") or pqs.get("trackasin") or [""])[0]
                    if not track_asin:
                        mm=re.search(r"/(?:tracks|music/player/tracks)/(B[0-9A-Z]{9})",pu.path or "",re.I)
                        if mm: track_asin=mm.group(1)
                    if track_asin: break
                except Exception:
                    pass

            chunks=[]
            if track_asin:
                for m in re.finditer(re.escape(track_asin),html,re.I):
                    chunks.append(html[max(0,m.start()-20000):min(len(html),m.end()+20000)])
                    if len(chunks)>=8: break
            chunks.append(html)
            for chunk in chunks:
                # Amazon has used title/name/trackTitle and artistName/contributors in different builds.
                if not title:
                    for pat in (r'"trackTitle"\s*:\s*"((?:\\.|[^"\\])+)"',
                                r'"title"\s*:\s*"((?:\\.|[^"\\])+)"',
                                r'"name"\s*:\s*"((?:\\.|[^"\\])+)"'):
                        mm=re.search(pat,chunk,re.I)
                        if mm:
                            cand=_usable(mm.group(1))
                            if cand and len(cand)<300:
                                title=cand; break
                if not artist:
                    for pat in (r'"artistName"\s*:\s*"((?:\\.|[^"\\])+)"',
                                r'"displayArtistName"\s*:\s*"((?:\\.|[^"\\])+)"',
                                r'"artists"\s*:\s*\[\s*\{[^{}]{0,1200}?"name"\s*:\s*"((?:\\.|[^"\\])+)"',
                                r'"artist"\s*:\s*\{[^{}]{0,1200}?"name"\s*:\s*"((?:\\.|[^"\\])+)"'):
                        mm=re.search(pat,chunk,re.I|re.S)
                        if mm:
                            artist=_clean(mm.group(1)); break
                if title and artist: break

            clean=_usable(title)
            clean=re.sub(r"\s*(?:on|–|-)\s*Amazon Music.*$","",clean,flags=re.I).strip()
            # Common title shapes: "Song by Artist" / "Song - Artist".
            if not artist and clean:
                m=re.match(r"(.+?)\s+by\s+(.+)$",clean,re.I)
                if m:
                    clean,artist=m.group(1).strip(),m.group(2).strip()
            if not artist and desc:
                for pat in (r"(?:song|track)\s+by\s+([^|.,]{2,120})", r"\bby\s+([^|.,]{2,120})"):
                    m=re.search(pat,desc,re.I)
                    if m:
                        artist=m.group(1).strip(); break
            title=clean
            if title and artist:
                return {"index":1,"title":title,"artist":artist,"album":album,
                        "query":f"{title} {artist}".strip(),"cover_url":cover or None}

        msg=("Amazon Musicの共有リンクから曲名・アーティストを取得できませんでした。\n"
             "短縮リンクにも対応しましたが、Amazon側がメタデータを返さないリンクの場合があります。") if self.lang=="ja" else (
             "Could not resolve title/artist from this Amazon Music share link. Short links are supported, but some Amazon pages do not expose metadata.")
        if last_error: msg += f"\n{last_error}"
        raise RuntimeError(msg)

    def _music_match_prepare_urls(self,urls):
        """Resolve Apple Music / Amazon Music metadata, then prepare YouTube Music matching queries."""
        out=[]
        meta_list=[]
        service=getattr(self,"download_service","music_match")
        for raw in urls:
            url=raw.strip()
            if not url:
                continue
            low=url.lower()
            if "music.youtube.com/" in low or (("youtube.com/" in low or "youtu.be/" in low) and ("list=" in low or "watch" in low)):
                out.append(url); meta_list.append(None); continue
            looks_url=low.startswith("http://") or low.startswith("https://")
            if looks_url and service=="apple_music" and "music.apple.com/" in low:
                self._post_dl_ui("status", "Apple Music情報を取得中..." if self.lang=="ja" else "Fetching Apple Music metadata...")
                entries=self._apple_music_entries(url)
                if not entries:
                    raise RuntimeError("Apple Musicの曲/アルバム情報を取得できませんでした。" if self.lang=="ja" else "Could not resolve Apple Music metadata.")
                for e in entries:
                    out.append(f"ytsearch1:{e['query']}"); meta_list.append(e)
                continue
            if looks_url and service=="amazon_music":
                self._post_dl_ui("status", "Amazon Music曲情報を取得中..." if self.lang=="ja" else "Fetching Amazon Music metadata...")
                e=self._amazon_music_entry(url)
                out.append(f"ytsearch1:{e['query']}"); meta_list.append(e)
                continue
            # Plain text input remains supported.
            if not looks_url:
                title=url.strip()
                e={"index":len(meta_list)+1,"title":title,"artist":"","album":"","query":title,"cover_url":None}
                out.append(f"ytsearch1:{title}"); meta_list.append(e); continue
            # Generic fallback for other public music links: read OpenGraph title.
            html=self._spotify_http_get(url,timeout=15)
            title=self._html_meta_content(html,"og:title") or self._html_meta_content(html,"twitter:title","name")
            title=re.sub(r"\s+"," ",html_unescape(title or "")).strip()
            if not title:
                raise RuntimeError("曲名を自動取得できませんでした。" if self.lang=="ja" else "Could not automatically resolve the title.")
            e={"index":len(meta_list)+1,"title":title,"artist":"","album":"","query":title,"cover_url":None}
            out.append(f"ytsearch1:{title}"); meta_list.append(e)
        self._dl_meta_list=meta_list
        return out

    def download_worker(self,url,folder,fmt,video_quality,audio_quality,meta=None,sample_rate=None):
        """
        Use the standalone yt-dlp executable bundled by the builder.
        This keeps YouTube/TikTok extractors current and avoids PyInstaller
        dynamic-extractor problems. YouTube also gets a bundled Deno runtime
        for yt-dlp's current EJS challenge solver.
        """
        os.makedirs(folder,exist_ok=True)

        ytdlp=tool("yt-dlp")
        if not ytdlp:
            raise RuntimeError(
                ("yt-dlp が見つかりません。WindowsはBUILD_EXE_ONE_CLICK.bat、MacはBUILD_MAC.commandを実行してください。" if self.lang=="ja" else "yt-dlp was not found. Run BUILD_EXE_ONE_CLICK.bat on Windows or BUILD_MAC.command on macOS.")
            )

        ff=tool("ffmpeg")
        deno=tool("deno")
        aq=re.sub(r"\D","",audio_quality) or "192"
        low=url.lower()
        is_youtube=("youtube.com/" in low or "youtu.be/" in low or "music.youtube.com/" in low)
        is_tiktok=("tiktok.com/" in low or "vm.tiktok.com/" in low or "vt.tiktok.com/" in low)
        is_spotify=("spotify.com/" in low or "spotify:" in low or "open.spotify.com/" in low)

        # Spotify track links are converted on the UI thread to ytsearch1:TITLE.
        # Episodes may still arrive as open.spotify.com URLs.
        download_url=url
        allow_playlist=bool(is_youtube and ("list=" in low or "/playlist" in low))
        playlist_meta=None
        if allow_playlist:
            try:
                playlist_meta=self._youtube_playlist_metadata(ytdlp, download_url, deno)
            except Exception:
                playlist_meta=None
        force_youtube_search=(
            url.startswith("ytsearch1:") or url.startswith("ytsearch:")
        )
        if force_youtube_search:
            is_youtube=True
            q=url.split(":",1)[-1]
            self._post_dl_ui(
                "status",
                (f"検索中: {q}" if self.lang=="ja" else f"Searching: {q}")[:80]
            )

        cmd=[
            ytdlp,
            "--newline",
            "--no-color",
            "--progress-template",
            "download:ATRACPROG|%(progress._percent_str)s|%(progress._speed_str)s|%(progress._eta_str)s",
            "--retries","5",
            "--fragment-retries","5",
            "--socket-timeout","30",
            "--no-continue",
            "--no-warnings",
        ]
        if os.name=="nt":
            cmd.append("--windows-filenames")
        # Numbered filename for playlist/album order; otherwise title
        if allow_playlist:
            out_tmpl=os.path.join(folder,"%(playlist_index)02d - %(title)s.%(ext)s")
        elif meta and meta.get("index") is not None:
            idx=int(meta.get("index") or 1)
            t=(meta.get("title") or "track").strip() or "track"
            t=re.sub(r'[<>:"/\\|?*]', "_", t)[:90]
            out_tmpl=os.path.join(folder, f"{idx:02d} - {t}.%(ext)s")
        else:
            out_tmpl=os.path.join(folder,"%(title)s.%(ext)s")
        cmd += ["-o", out_tmpl]
        if not allow_playlist:
            cmd.append("--no-playlist")

        if ff:
            ff_dir=os.path.dirname(os.path.abspath(ff))
            cmd += ["--ffmpeg-location", ff_dir if ff_dir else ff]
            # Also ensure ffprobe is discoverable beside ffmpeg
            probe=os.path.join(ff_dir,"ffprobe.exe" if os.name=="nt" else "ffprobe") if ff_dir else None
            if probe and os.path.exists(probe):
                pass  # yt-dlp finds ffprobe next to ffmpeg automatically

        # YouTube changes frequently.  Current yt-dlp needs a JS runtime for
        # challenge solving and may need explicit player clients to expose
        # normal downloadable HTTPS formats.  The official yt-dlp.exe already
        # bundles EJS, so do not depend on GitHub at runtime.
        # Prefer android/ios first — web-only clients often hit HTTP 403 on media URLs.
        if is_youtube or force_youtube_search:
            if deno:
                cmd += ["--js-runtimes", f"deno:{deno}"]
            if fmt=="MP4":
                cmd += ["--extractor-args","youtube:player_client=android,ios,tv,mweb,web"]
            cmd += [
                "--user-agent",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "--referer", "https://www.youtube.com/",
                "--add-header", "Accept-Language:ja,en-US;q=0.9,en;q=0.8",
                "--geo-bypass",
            ]

        # Browser-like headers improve public TikTok page extraction.
        if is_tiktok:
            cmd += [
                "--user-agent",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0 Safari/537.36",
                "--referer","https://www.tiktok.com/"
            ]

        if fmt=="MP4":
            if is_tiktok:
                form="bestvideo*+bestaudio/best"
            else:
                form=self._video_format_string(video_quality)
            cmd += ["-f",form,"--merge-output-format","mp4"]
            if not ff:
                # Without ffmpeg, avoid merge that requires it
                cmd += ["-f","best[ext=mp4]/best"]
        else:
            # Audio download — prefer the highest available source bitrate, then
            # re-encode to the user-selected format/bitrate. Low-quality picks
            # often came from weak format sorting or web-only clients.
            if ff:
                codec={"MP3":"mp3","M4A":"m4a","FLAC":"flac","ADTS (.adts)":"aac"}.get(fmt,"mp3")
                # Prefer pure audio streams sorted by average bitrate (abr).
                # Fall back to any best stream if separate audio is unavailable.
                cmd += [
                    "-f", "bestaudio/best",
                    "-S", "abr,asr,acodec",
                    "-x", "--audio-format", codec,
                ]
                if fmt == "FLAC":
                    # Lossless: do not force a lossy bitrate.
                    pass
                else:
                    # Fixed bitrate re-encode (e.g. 320K). yt-dlp accepts NNK.
                    cmd += ["--audio-quality", f"{aq}K"]
                # Keep source sample rate unless the user explicitly overrides it.
                if sample_rate:
                    cmd += ["--postprocessor-args",
                            f"ExtractAudio+ffmpeg:-af aresample=resampler=soxr:precision=28 -ar {sample_rate}"]
                if is_spotify or force_youtube_search or is_youtube or "music.youtube.com/" in low:
                    cmd += ["--embed-metadata", "--embed-thumbnail"]
            else:
                # No ffmpeg: keep original high-bitrate audio container.
                cmd += ["-f", "bestaudio[ext=m4a]/bestaudio/best", "-S", "abr"]

        cmd.append(download_url)

        # On HTTP 403, retry with alternate YouTube player clients. Web clients
        # frequently return 403 for media URLs while android/ios still work.
        client_attempts = []
        if is_youtube or force_youtube_search:
            if fmt!="MP4":
                # Audio: let yt-dlp pick its default clients first (they expose
                # the highest-bitrate Opus/AAC streams), then fall back.
                client_attempts = [None,"tv,mweb,web","web","android,ios"]
            else:
                client_attempts = [
                    "android,ios,tv,mweb,web",
                    "android,ios",
                    "tv,mweb",
                    "web",
                ]
        else:
            client_attempts = [None]

        flags=getattr(subprocess,"CREATE_NO_WINDOW",0)
        percent_re=re.compile(r"(\d+(?:\.\d+)?)%")
        speed_re=re.compile(r"at\s+([^\s]+)")
        eta_re=re.compile(r"ETA\s+([0-9:]+|Unknown|N/A)", re.I)
        last_error=None

        for attempt_i, clients in enumerate(client_attempts):
            if self._is_work_cancelled():
                raise RuntimeError("ダウンロードをキャンセルしました。" if self.lang=="ja" else "Download cancelled.")

            run_cmd=list(cmd)
            if clients is not None:
                # Replace any existing player_client extractor-args.
                cleaned=[]
                skip_next=False
                for i,arg in enumerate(run_cmd):
                    if skip_next:
                        skip_next=False
                        continue
                    if arg == "--extractor-args" and i+1 < len(run_cmd) and str(run_cmd[i+1]).startswith("youtube:player_client="):
                        skip_next=True
                        continue
                    cleaned.append(arg)
                run_cmd=cleaned
                run_cmd += ["--extractor-args", f"youtube:player_client={clients}"]
                if attempt_i > 0:
                    self._post_dl_ui(
                        "status",
                        (f"再試行中 ({clients.split(',')[0]})..." if self.lang=="ja"
                         else f"Retrying ({clients.split(',')[0]})...")
                    )

            p=subprocess.Popen(
                run_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=flags
            )
            self._track_proc(p)

            last_lines=[]
            try:
                for line in p.stdout:
                    if self._is_work_cancelled():
                        try:
                            self._kill_process(p, timeout=1.0)
                        except Exception:
                            pass
                        raise RuntimeError("ダウンロードをキャンセルしました。" if self.lang=="ja" else "Download cancelled.")
                    line=line.strip()
                    if not line:
                        continue
                    last_lines.append(line)
                    if len(last_lines)>20:
                        last_lines.pop(0)

                    if line.startswith("ATRACPROG|"):
                        parts=line.split("|",3)
                        pct=0.0
                        speed="-"
                        eta="-"
                        if len(parts) > 1:
                            m=percent_re.search(parts[1])
                            if m:
                                try: pct=float(m.group(1))
                                except Exception: pct=0.0
                        if len(parts) > 2:
                            speed=parts[2].strip() or "-"
                        if len(parts) > 3:
                            eta=parts[3].strip() or "-"
                        self._post_dl_ui("progress",pct,speed,eta)
                        continue

                    m=percent_re.search(line)
                    if m:
                        try:
                            pct=float(m.group(1))
                        except Exception:
                            pct=0.0
                        sm=speed_re.search(line)
                        em=eta_re.search(line)
                        speed=sm.group(1) if sm else "-"
                        eta=em.group(1) if em else "-"
                        self._post_dl_ui("progress",pct,speed,eta)
                    elif "ExtractAudio" in line or "Merger" in line or "Remux" in line:
                        self._post_dl_ui(
                            "status",
                            (f"{self.dl_batch_index}/{self.dl_batch_total}  " if self.dl_batch_total>1 else "") +
                            ("変換中..." if self.lang=="ja" else "Converting...")
                        )

                rc=p.wait()
            finally:
                self._untrack_proc(p)

            if self._is_work_cancelled():
                raise RuntimeError("ダウンロードをキャンセルしました。" if self.lang=="ja" else "Download cancelled.")

            if rc==0:
                last_error=None
                break

            detail="\n".join(last_lines[-8:]) or f"yt-dlp exit code {rc}"
            last_error=RuntimeError(detail)
            # Retry only on typical YouTube access/403 failures.
            low_detail=detail.lower()
            if not (is_youtube or force_youtube_search):
                raise last_error
            if not any(x in low_detail for x in ("403", "forbidden", "http error", "unable to download", "sign in", "confirm you're not a bot")):
                raise last_error
            # else continue to next client attempt

        if last_error is not None:
            raise last_error

        # Apply playlist order/title/artist/album after a YouTube playlist download.
        if allow_playlist and ff and playlist_meta:
            try:
                self._tag_youtube_playlist_files(folder, playlist_meta, ff)
            except Exception:
                pass

        # Embed Spotify cover + track/album metadata when available
        if meta and ff:
            try:
                self._spotify_tag_downloaded(folder, meta, ff, last_lines)
            except Exception:
                pass

        self._post_dl_ui("progress",100,None,0)

    def _youtube_playlist_metadata(self,ytdlp,url,deno=None):
        """Read YouTube playlist title/order and best-effort artist names before download."""
        cmd=[ytdlp,"--flat-playlist","--dump-single-json","--no-warnings"]
        if deno:
            cmd += ["--js-runtimes",f"deno:{deno}"]
        cmd += ["--remote-components","ejs:github",url]
        flags=getattr(subprocess,"CREATE_NO_WINDOW",0)
        r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding="utf-8",errors="replace",creationflags=flags)
        if r.returncode!=0 or not r.stdout.strip():
            return None
        data=json.loads(r.stdout)
        album=(data.get("title") or data.get("playlist_title") or "YouTube Playlist").strip()
        entries=[]
        for i,e in enumerate(data.get("entries") or [],1):
            if not isinstance(e,dict):
                continue
            title=str(e.get("title") or f"Track {i}").strip()
            artist=str(e.get("artist") or e.get("uploader") or e.get("channel") or e.get("creator") or "").strip()
            entries.append({"index":i,"title":title,"artist":artist,"album":album})
        return {"album":album,"entries":entries}

    def _tag_youtube_playlist_files(self,folder,playlist_meta,ff):
        """Tag downloaded playlist files: track number, title, artist and playlist name as album."""
        entries=(playlist_meta or {}).get("entries") or []
        for item in entries:
            idx=int(item.get("index") or 1)
            prefix=f"{idx:02d} - "
            try:
                cands=[os.path.join(folder,n) for n in os.listdir(folder)
                       if n.startswith(prefix) and n.lower().endswith((".mp3",".m4a",".flac",".aac",".opus",".ogg",".webm",".mp4",".mkv"))]
            except Exception:
                cands=[]
            if not cands:
                continue
            cands.sort(key=lambda x: os.path.getmtime(x),reverse=True)
            dest=cands[0]
            tags={
                "track":str(idx),
                "title":str(item.get("title") or "").strip(),
                "album":str(item.get("album") or (playlist_meta or {}).get("album") or "").strip(),
            }
            artist=str(item.get("artist") or "").strip()
            if artist:
                tags["artist"]=artist
            tags={k:v for k,v in tags.items() if v}
            if tags:
                try:
                    write_tags(ff,dest,tags)
                except Exception:
                    pass

    def _spotify_tag_downloaded(self,folder,meta,ff,last_lines=None):
        """Apply track number / title / artist / album / cover using mutagen (reliable for MP3)."""
        if not meta:
            return

        dest=None
        # 1) yt-dlp Destination line
        for line in reversed(last_lines or []):
            m=re.search(r"Destination:\s*(.+)$", line)
            if m:
                cand=m.group(1).strip().strip('"')
                if os.path.exists(cand):
                    dest=cand
                    break
            m=re.search(r"\[download\]\s+(.+?) has already been downloaded", line)
            if m:
                cand=m.group(1).strip()
                if os.path.exists(cand):
                    dest=cand
                    break

        # 2) Numbered filename we requested
        if not dest:
            idx=int(meta.get("index") or 1)
            t=(meta.get("title") or "track").strip() or "track"
            t=re.sub(r'[<>:"/\\|?*]', "_", t)[:90]
            prefix=f"{idx:02d} - {t}"
            try:
                cands=[]
                for name in os.listdir(folder):
                    low=name.lower()
                    if not low.endswith((".mp3",".m4a",".flac",".opus",".webm",".ogg",".mp4",".mkv")):
                        continue
                    if name.startswith(prefix+".") or name.startswith(prefix+" "):
                        cands.append(os.path.join(folder, name))
                if cands:
                    # newest file wins
                    cands.sort(key=lambda p: os.path.getmtime(p), reverse=True)
                    dest=cands[0]
            except Exception:
                pass

        # 3) newest audio file in folder (last resort for single-track)
        if not dest:
            try:
                cands=[]
                for name in os.listdir(folder):
                    low=name.lower()
                    if low.endswith((".mp3",".m4a",".flac",".opus",".webm",".ogg")):
                        cands.append(os.path.join(folder, name))
                if cands:
                    cands.sort(key=lambda p: os.path.getmtime(p), reverse=True)
                    dest=cands[0]
            except Exception:
                pass

        if not dest or not os.path.exists(dest):
            return

        # Download cover to a temp JPEG
        cover_path=None
        cover_url=meta.get("cover_url")
        if cover_url:
            data=None
            for unverified in (False, True):
                try:
                    if unverified:
                        ctx=ssl._create_unverified_context()
                    else:
                        ctx=ssl.create_default_context()
                        try:
                            import certifi
                            ctx=ssl.create_default_context(cafile=certifi.where())
                        except Exception:
                            pass
                    req=urllib.request.Request(
                        cover_url,
                        headers={
                            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                            "Accept":"image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                        },
                    )
                    with urllib.request.urlopen(req, timeout=25, context=ctx) as resp:
                        data=resp.read()
                    if data:
                        break
                except Exception:
                    data=None
            if data:
                try:
                    cover_path=os.path.join(
                        tempfile.gettempdir(),
                        f"atrac_sp_cover_{os.getpid()}_{meta.get('index',0)}.jpg",
                    )
                    # Normalize via PIL so mutagen always gets JPEG
                    import io
                    from PIL import Image
                    im=Image.open(io.BytesIO(data))
                    if im.mode not in ("RGB","L"):
                        im=im.convert("RGB")
                    elif im.mode=="L":
                        im=im.convert("RGB")
                    im.thumbnail((1200,1200))
                    im.save(cover_path, format="JPEG", quality=90)
                except Exception:
                    # raw write fallback
                    try:
                        with open(cover_path,"wb") as f:
                            f.write(data)
                    except Exception:
                        cover_path=None

        tags={}
        if meta.get("title"):
            tags["title"]=str(meta.get("title")).strip()
        if meta.get("artist"):
            tags["artist"]=str(meta.get("artist")).strip()
        if meta.get("album"):
            tags["album"]=str(meta.get("album")).strip()
        if meta.get("index") is not None:
            tags["track"]=str(meta.get("index"))

        try:
            if tags and ff:
                write_tags(ff, dest, tags)
        except Exception:
            pass

        if cover_path and os.path.exists(cover_path):
            try:
                _replace_cover_art(dest, cover_path)
            except Exception:
                # last resort: ffmpeg attach
                try:
                    if ff:
                        out_tmp=dest+".__cover__"+os.path.splitext(dest)[1]
                        cmd=[
                            ff,"-y","-hide_banner","-loglevel","error",
                            "-i",dest,"-i",cover_path,
                            "-map","0:a","-map","1",
                            "-c","copy","-disposition:v:0","attached_pic",
                            "-id3v2_version","3",
                        ]
                        for k,v in tags.items():
                            cmd += ["-metadata", f"{k}={v}"]
                        cmd.append(out_tmp)
                        flags=getattr(subprocess,"CREATE_NO_WINDOW",0)
                        r=subprocess.run(cmd, capture_output=True, creationflags=flags)
                        if r.returncode==0 and os.path.exists(out_tmp):
                            os.replace(out_tmp, dest)
                        elif os.path.exists(out_tmp):
                            os.remove(out_tmp)
                except Exception:
                    pass
            try:
                os.remove(cover_path)
            except Exception:
                pass

    def _reset_dl_ui(self):
        self._dl_progress_value=0.0
        try:
            if self.onprog is not None and self.onprog.winfo_exists():
                self.onprog["value"]=0
        except Exception:
            pass
        prefix=(f"{self.dl_batch_index}/{self.dl_batch_total}  " if self.dl_batch_total>1 else "")
        try:self.dl_percent.set(prefix+"0%")
        except Exception:pass
        try:self.dl_speed.set("-")
        except Exception:pass
        try:self.dl_eta.set("-")
        except Exception:pass

    def _add_cancel_button(self,parent,command=None,enabled=None):
        p=self.p()
        b=ctk.CTkButton(parent,text=("■ キャンセル" if self.lang=="ja" else "■ Cancel"),
                        command=command or self.cancel_download,width=120,
                        fg_color=p["panel2"],hover_color=p["danger"],text_color=p["danger"],
                        border_width=1,border_color=p["danger"],corner_radius=12,height=38,
                        font=("Segoe UI",11,"bold"))
        b.pack(side="right",padx=(0,8))
        try:
            active=self.download_active if enabled is None else bool(enabled)
            b.configure(state="normal" if active else "disabled")
        except Exception:
            pass
        self.cancelbtn=b
        return b

    def _set_cancel_state(self,enabled):
        try:
            if self.cancelbtn is not None and self.cancelbtn.winfo_exists():
                self.cancelbtn.configure(state="normal" if enabled else "disabled")
        except Exception:
            pass

    def _cancel_tracked_processes_async(self):
        def _kill():
            try:
                with self._tracked_procs_lock:
                    procs=list(self._tracked_procs)
                for pr in procs:
                    try: self._kill_process(pr,timeout=1.0)
                    except Exception: pass
            except Exception:
                pass
        threading.Thread(target=_kill,daemon=True).start()

    def cancel_operation(self):
        if self._user_cancelled or self._is_work_cancelled():
            return
        self._user_cancelled=True
        try: self._cancel_work.set()
        except Exception: pass
        self._set_cancel_state(False)
        self._cancel_tracked_processes_async()

    def cancel_download(self):
        """User pressed Cancel: stop yt-dlp / ffmpeg and reset the UI quietly."""
        if not self.download_active or self._user_cancelled:
            return
        self._user_cancelled=True
        try: self._cancel_work.set()
        except Exception: pass
        self._set_cancel_state(False)
        try: self.dl_percent.set("キャンセル中..." if self.lang=="ja" else "Cancelling...")
        except Exception: pass
        self._cancel_tracked_processes_async()

    def _cleanup_partial_downloads(self):
        """Remove unfinished .part/.ytdl files created by the cancelled run."""
        try:
            folder=self.online_folder.get().strip() or self._library_download_dir()
            since=float(getattr(self,"_dl_started_at",0.0) or 0.0)-2
            for root_dir,_,files in os.walk(folder):
                for fn in files:
                    if fn.endswith((".part",".ytdl",".temp")) or ".part-Frag" in fn:
                        fp=os.path.join(root_dir,fn)
                        try:
                            if os.path.getmtime(fp)>=since: os.remove(fp)
                        except Exception: pass
        except Exception:
            pass

    def _clear_downloaded_urls(self):
        """After a fully successful download, remove the submitted URLs from the input box.
        Lines the user typed while downloading are kept."""
        done={u.strip() for u in (getattr(self,"_dl_submitted",None) or []) if u.strip()}
        if not done:
            return
        def strip_lines(text):
            keep=[ln for ln in text.splitlines() if ln.strip() and ln.strip() not in done]
            return "\n".join(keep)
        svc=getattr(self,"_dl_service_key",None)
        try:
            if svc in self.service_urls:
                self.service_urls[svc]=strip_lines(self.service_urls.get(svc,""))
        except Exception:
            pass
        try:
            w=getattr(self,"online_text",None)
            if (w is not None and w.winfo_exists()
                    and getattr(self,"download_service",None)==svc):
                rest=strip_lines(w.get("1.0","end-1c"))
                w.delete("1.0","end")
                if rest:
                    w.insert("1.0",rest)
                if svc in self.service_urls:
                    self.service_urls[svc]=rest
        except Exception:
            pass
        self._dl_submitted=[]

    def _download_success(self):
        self.download_active=False
        self._set_cancel_state(False)
        try:
            self._clear_downloaded_urls()
        except Exception:
            pass
        self._dl_progress_value=100.0
        try:
            if self.onprog is not None and self.onprog.winfo_exists():
                self.onprog["value"]=100
        except Exception:
            pass
        prefix=(f"{self.dl_batch_total}/{self.dl_batch_total}  " if self.dl_batch_total>1 else "")
        try:self.dl_percent.set(prefix+"100%")
        except Exception:pass
        try:
            if self.downbtn is not None and self.downbtn.winfo_exists():
                self.downbtn.configure(state="normal")
        except Exception:
            pass
        # Refresh the library only when that page is open; the file is already
        # safely stored even if the user is on another page.
        try:
            if getattr(self,"current_page",None)=="library":
                self._library_refresh()
        except Exception:
            pass
        messagebox.showinfo(APP_NAME,self.tr("batch_download_done"))
        self.dl_batch_index=1
        self.dl_batch_total=1
        self._reset_dl_ui()

    def _download_error(self,msg):
        self.download_active=False
        self._set_cancel_state(False)
        try:
            if self.downbtn is not None and self.downbtn.winfo_exists():
                self.downbtn.configure(state="normal")
        except Exception:
            pass
        if getattr(self,"_user_cancelled",False):
            # Quiet reset: no error dialog when the user cancelled on purpose.
            self._user_cancelled=False
            try: self._cancel_work.clear()
            except Exception: pass
            self._cleanup_partial_downloads()
            self._dl_progress_value=0.0
            try:
                if self.onprog is not None and self.onprog.winfo_exists():
                    self.onprog["value"]=0
            except Exception:
                pass
            self.dl_batch_index=1; self.dl_batch_total=1
            try: self.dl_percent.set("キャンセルしました" if self.lang=="ja" else "Cancelled")
            except Exception: pass
            try: self.dl_speed.set("-"); self.dl_eta.set("-")
            except Exception: pass
            return
        messagebox.showerror(APP_NAME,msg)



    # ------------------------------------------------------------------
    # Batch folder rename only (files inside folders are never renamed)
    # ------------------------------------------------------------------
    def _safe_folder_name(self, name):
        name=str(name or "").strip()
        name=re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", name)
        name=name.rstrip(" .")
        return name

    def _two_stage_rename_paths(self, plan):
        """plan: list of (src Path, dst Path) for folders or files."""
        temp_plan=[]
        try:
            for idx,(src,dst) in enumerate(plan):
                src=Path(src); dst=Path(dst)
                if os.path.normcase(os.path.abspath(str(src))) == os.path.normcase(os.path.abspath(str(dst))):
                    temp_plan.append((src,src,dst))
                    continue
                tmp=src.with_name(f".__atrac_rename_{uuid.uuid4().hex}_{idx}")
                src.rename(tmp)
                temp_plan.append((src,tmp,dst))
            renamed=[]
            for original,tmp,dst in temp_plan:
                if tmp != original or dst != original:
                    if dst.exists() and os.path.normcase(os.path.abspath(str(dst))) != os.path.normcase(os.path.abspath(str(tmp))):
                        raise RuntimeError(f"Already exists: {dst}")
                    tmp.rename(dst)
                renamed.append(str(dst))
            return renamed
        except Exception:
            for original,tmp,dst in reversed(temp_plan):
                try:
                    if Path(tmp).exists() and not Path(original).exists():
                        Path(tmp).rename(original)
                    elif Path(dst).exists() and not Path(original).exists():
                        Path(dst).rename(original)
                except Exception:
                    pass
            raise

    def page_mtime_editor(self):
        """Edit filesystem modified time for selected files and folders."""
        p=self.p()

        top=self.card(self.content); top.pack(fill="x",pady=(0,12))
        hdr=tk.Frame(top,bg=p["panel"]); hdr.pack(fill="x",padx=18,pady=14)
        tk.Label(
            hdr,
            text=("フォルダー / ファイル 更新時間編集" if self.lang=="ja" else "File / Folder Modified Time Editor"),
            font=("Segoe UI",16,"bold"),bg=p["panel"],fg=p["text"]
        ).pack(side="left")
        tk.Label(
            hdr,
            text=("ファイルやフォルダーそのものの更新日時を変更します" if self.lang=="ja" else "Change the filesystem modified time of files and folders"),
            font=("Segoe UI",9),bg=p["panel"],fg=p["muted"]
        ).pack(side="left",padx=12)

        panel=self.card(self.content); panel.pack(fill="both",expand=True)

        toolbar=tk.Frame(panel,bg=p["panel"]); toolbar.pack(fill="x",padx=16,pady=(16,8))

        def refresh_list():
            self.mtime_listbox.delete(0,"end")
            for path in self.mtime_items:
                try:
                    ts=os.path.getmtime(path)
                    shown=datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    shown="?"
                kind=("[フォルダー]" if os.path.isdir(path) else "[ファイル]") if self.lang=="ja" else ("[Folder]" if os.path.isdir(path) else "[File]")
                self.mtime_listbox.insert("end",f"{kind}  {shown}  |  {path}")

        def add_paths(paths):
            changed=False
            for path in paths:
                path=os.path.abspath(str(path))
                if os.path.exists(path) and path not in self.mtime_items:
                    self.mtime_items.append(path); changed=True
            if changed: refresh_list()

        def add_files():
            files=filedialog.askopenfilenames(title=("ファイルを追加" if self.lang=="ja" else "Add files"),filetypes=[("All","*.*")])
            if files: add_paths(files)

        def add_folder():
            folder=filedialog.askdirectory(title=("フォルダーを追加" if self.lang=="ja" else "Add folder"))
            if folder: add_paths([folder])

        def remove_selected():
            sel=list(self.mtime_listbox.curselection())
            for i in reversed(sel):
                if 0 <= i < len(self.mtime_items):
                    self.mtime_items.pop(i)
            refresh_list()

        def clear_all():
            self.mtime_items.clear(); refresh_list()

        for txt,cmd,primary in [
            (("+ ファイル追加" if self.lang=="ja" else "+ Add Files"),add_files,True),
            (("+ フォルダー追加" if self.lang=="ja" else "+ Add Folder"),add_folder,True),
            (("選択した項目を消去" if self.lang=="ja" else "Remove Selected"),remove_selected,False),
            (("全消去" if self.lang=="ja" else "Clear All"),clear_all,False),
        ]:
            b=ctk.CTkButton(toolbar,text=txt,command=cmd); self.style_button(b,primary); b.pack(side="left",padx=(0,8))

        dropframe=tk.Frame(panel,bg=p["panel2"],highlightthickness=1,highlightbackground=p["line"])
        dropframe.pack(fill="both",expand=True,padx=16,pady=(0,12))
        tk.Label(
            dropframe,
            text=("ここにファイル / フォルダーをドラッグ＆ドロップ" if self.lang=="ja" else "Drag & drop files / folders here"),
            bg=p["panel2"],fg=p["muted"],font=("Segoe UI",10,"bold")
        ).pack(anchor="w",padx=12,pady=(10,4))
        self.mtime_listbox=tk.Listbox(
            dropframe,bg=p["entry"],fg=p["text"],selectbackground=p["accent"],
            relief="flat",bd=0,height=16,font=("Segoe UI",10)
        )
        self.mtime_listbox.pack(fill="both",expand=True,padx=10,pady=(0,10))
        refresh_list()
        self._enable_drop(self.mtime_listbox,add_paths)
        self._enable_drop(dropframe,add_paths)

        edit=self.card(panel); edit.pack(fill="x",padx=16,pady=(0,16))

        # Folder handling: the selected folder itself is always updated.  When
        # enabled, every file/subfolder inside it is also updated recursively.
        self.mtime_recursive_var=tk.BooleanVar(value=False)
        recurse_row=tk.Frame(edit,bg=p["panel"]); recurse_row.pack(fill="x",padx=14,pady=(12,0))
        ctk.CTkCheckBox(
            recurse_row,
            text=("フォルダー内のファイル・サブフォルダーも変更" if self.lang=="ja" else "Also change files and subfolders inside folders"),
            variable=self.mtime_recursive_var
        ).pack(side="left")

        row=tk.Frame(edit,bg=p["panel"]); row.pack(fill="x",padx=14,pady=14)
        tk.Label(
            row,text=("新しい更新日時" if self.lang=="ja" else "New modified time"),
            bg=p["panel"],fg=p["text"],font=("Segoe UI",10,"bold")
        ).pack(side="left")
        entry=tk.Entry(
            row,textvariable=self.mtime_value,width=24,relief="flat",bd=0,
            bg=p["entry"],fg=p["text"],insertbackground=p["text"],font=("Segoe UI",11)
        )
        entry.pack(side="left",padx=(12,8),ipady=7)
        tk.Label(
            row,text=("YYYY-MM-DD HH:MM:SS" if self.lang=="ja" else "YYYY-MM-DD HH:MM:SS"),
            bg=p["panel"],fg=p["muted"],font=("Segoe UI",9)
        ).pack(side="left",padx=(0,12))

        def set_now():
            self.mtime_value.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        now_btn=ctk.CTkButton(row,text=("現在時刻" if self.lang=="ja" else "Now"),command=set_now,width=90)
        self.style_button(now_btn,False); now_btn.pack(side="left",padx=(0,8))

        status=tk.Label(edit,text="",bg=p["panel"],fg=p["muted"],font=("Segoe UI",9))
        status.pack(anchor="w",padx=14,pady=(0,12))

        def apply_time():
            if not self.mtime_items:
                return messagebox.showwarning(APP_NAME,("ファイルまたはフォルダーを追加してください。" if self.lang=="ja" else "Add a file or folder first."),parent=self.root)
            raw=self.mtime_value.get().strip()
            parsed=None
            for fmt in ("%Y-%m-%d %H:%M:%S","%Y-%m-%d %H:%M"):
                try:
                    parsed=datetime.strptime(raw,fmt); break
                except ValueError:
                    pass
            if parsed is None:
                return messagebox.showerror(APP_NAME,("更新日時は YYYY-MM-DD HH:MM:SS 形式で入力してください。\n例: 2026-10-03 13:30:00" if self.lang=="ja" else "Use YYYY-MM-DD HH:MM:SS.\nExample: 2026-10-03 13:30:00"),parent=self.root)
            timestamp=parsed.timestamp()
            ok=[]; failures=[]

            # Build the exact filesystem targets.  A folder itself is always
            # included; recursive mode additionally includes every child.
            targets=[]
            seen=set()
            for path in list(self.mtime_items):
                ap=os.path.abspath(os.path.normpath(path))
                key=os.path.normcase(ap)
                if key not in seen:
                    seen.add(key); targets.append(ap)
                if os.path.isdir(ap) and bool(self.mtime_recursive_var.get()):
                    try:
                        for root_dir, dirs, files in os.walk(ap):
                            for name in files:
                                child=os.path.join(root_dir,name)
                                ck=os.path.normcase(os.path.abspath(child))
                                if ck not in seen:
                                    seen.add(ck); targets.append(child)
                            for name in dirs:
                                child=os.path.join(root_dir,name)
                                ck=os.path.normcase(os.path.abspath(child))
                                if ck not in seen:
                                    seen.add(ck); targets.append(child)
                    except Exception as e:
                        failures.append(f"{ap}: {e}")

            # Set children first and folders last.  This prevents walking or
            # touching children from changing a folder timestamp again after
            # we already set it.
            targets.sort(key=lambda x: (0 if os.path.isfile(x) else 1, -x.count(os.sep)))
            for path in targets:
                try:
                    st=os.stat(path, follow_symlinks=False)
                    try:
                        os.utime(path,(st.st_atime,timestamp),follow_symlinks=False)
                    except (TypeError, NotImplementedError, ValueError):
                        os.utime(path,(st.st_atime,timestamp))
                    ok.append(path)
                except Exception as e:
                    failures.append(f"{path}: {e}")
            refresh_list()
            if failures:
                status.config(text=((f"{len(ok)} 件成功 / {len(failures)} 件失敗" if self.lang=="ja" else f"{len(ok)} succeeded / {len(failures)} failed")))
                messagebox.showwarning(APP_NAME,("一部の更新時間を変更できませんでした。\n\n" if self.lang=="ja" else "Some modified times could not be changed.\n\n")+"\n".join(failures[:12]),parent=self.root)
            else:
                status.config(text=((f"{len(ok)} 件の更新時間を変更しました。" if self.lang=="ja" else f"Changed modified time for {len(ok)} items.")))
                messagebox.showinfo(APP_NAME,(f"{len(ok)} 件の更新時間を変更しました。" if self.lang=="ja" else f"Changed modified time for {len(ok)} items."),parent=self.root)

        apply_btn=ctk.CTkButton(edit,text=("更新時間を変更" if self.lang=="ja" else "Apply Modified Time"),command=apply_time)
        self.style_button(apply_btn,True); apply_btn.pack(anchor="e",padx=14,pady=(0,14))

    def page_batch_rename(self):
        """Rename folders only. Files inside those folders are left unchanged."""
        p=self.p()
        top=self.card(self.content); top.pack(fill="x", pady=(0,12))
        hdr=tk.Frame(top, bg=p["panel"]); hdr.pack(fill="x", padx=18, pady=14)
        tk.Label(hdr, text=("一括フォルダー名編集" if self.lang=="ja" else "Batch Folder Rename"),
                 font=("Segoe UI",16,"bold"), bg=p["panel"], fg=p["text"]).pack(side="left")
        tk.Label(hdr, text=("フォルダー名だけ変更（中のファイルは一切変更しません）" if self.lang=="ja"
                            else "Rename folders only — files inside are never touched"),
                 font=("Segoe UI",9), bg=p["panel"], fg=p["muted"]).pack(side="left", padx=12)

        def add_folders():
            # Multiple folders: askdirectory is single; loop via repeated or multi via DnD.
            folder=filedialog.askdirectory(title=("フォルダーを追加" if self.lang=="ja" else "Add folder"))
            if folder:
                self._batch_rename_add_folders([folder])
        def remove_sel():
            if not hasattr(self, "batch_rename_list"):
                return
            for i in reversed(self.batch_rename_list.curselection()):
                try:
                    self.rename_folders.pop(i)
                except Exception:
                    pass
                self.batch_rename_list.delete(i)
        def clear_all():
            self.rename_folders.clear()
            if hasattr(self, "batch_rename_list"):
                self.batch_rename_list.delete(0, "end")

        for txt, cmd, primary in [
            (("+ フォルダー追加" if self.lang=="ja" else "+ Add Folder"), add_folders, True),
            (("選択削除" if self.lang=="ja" else "Remove"), remove_sel, False),
            (("全消去" if self.lang=="ja" else "Clear"), clear_all, False),
        ]:
            b=ctk.CTkButton(hdr, text=txt, command=cmd); self.style_button(b, primary)
            b.pack(side="right", padx=(8,0))

        body=self.card(self.content); body.pack(fill="both", expand=True)

        note=tk.Label(
            body,
            text=("※ フォルダーの名前だけを連番で変更します。フォルダー内のファイル名・中身は変更しません。"
                  if self.lang=="ja" else
                  "* Only folder names are renamed sequentially. Files inside are not renamed or moved."),
            bg=p["panel"], fg=p["muted"], font=("Segoe UI",9), justify="left"
        )
        note.pack(anchor="w", padx=16, pady=(14,6))

        pattern=tk.Frame(body, bg=p["panel2"]); pattern.pack(fill="x", padx=16, pady=(0,10))
        tk.Label(pattern, text=("共通名" if self.lang=="ja" else "Base name"),
                 bg=p["panel2"], fg=p["text"], font=("Segoe UI",10,"bold")).pack(side="left", padx=(12,6), pady=10)
        tk.Entry(pattern, textvariable=self.rename_prefix, relief="flat", bd=0, width=28,
                 bg=p["entry"], fg=p["text"], insertbackground=p["text"]).pack(side="left", ipady=6)
        tk.Label(pattern, text=("開始" if self.lang=="ja" else "Start"),
                 bg=p["panel2"], fg=p["text"]).pack(side="left", padx=(12,4))
        tk.Entry(pattern, textvariable=self.rename_start, relief="flat", bd=0, width=6,
                 bg=p["entry"], fg=p["text"], insertbackground=p["text"]).pack(side="left", ipady=6)
        tk.Label(pattern, text=("桁数" if self.lang=="ja" else "Digits"),
                 bg=p["panel2"], fg=p["text"]).pack(side="left", padx=(12,4))
        ttk.Combobox(pattern, textvariable=self.rename_digits, state="readonly",
                     values=["1","2","3","4"], width=4).pack(side="left")
        tk.Label(pattern,
                 text=("例: ALBUM + 01 → ALBUM01（中の曲ファイル名はそのまま）" if self.lang=="ja"
                       else "e.g. ALBUM + 01 → ALBUM01 (files inside keep their names)"),
                 bg=p["panel2"], fg=p["muted"], font=("Segoe UI",9)).pack(side="left", padx=12)

        drop_hint=tk.Label(
            body,
            text=("ここにフォルダーをドラッグ＆ドロップ（複数可）" if self.lang=="ja"
                  else "Drag & drop folders here (multiple OK)"),
            bg=p["panel"], fg=p["muted"], font=("Segoe UI",9,"bold")
        )
        drop_hint.pack(anchor="w", padx=16, pady=(0,4))

        self.batch_rename_list=tk.Listbox(
            body, selectmode="extended", relief="flat", bd=0, highlightthickness=0,
            font=("Segoe UI",10), bg=p["panel2"], fg=p["text"], selectbackground=p["accent"]
        )
        self.batch_rename_list.pack(fill="both", expand=True, padx=16, pady=(0,12))
        for f in self.rename_folders:
            self.batch_rename_list.insert("end", f)
        self._enable_drop(self.batch_rename_list, self._batch_rename_add_folders)

        foot=tk.Frame(body, bg=p["panel"]); foot.pack(fill="x", padx=16, pady=(0,16))
        b=ctk.CTkButton(foot, text=("フォルダー名を一括変更" if self.lang=="ja" else "Rename Folders"),
                        command=self._batch_rename_apply)
        self.style_button(b, True); b.pack(side="right")
        b2=ctk.CTkButton(foot, text=("プレビュー" if self.lang=="ja" else "Preview"),
                         command=self._batch_rename_preview)
        self.style_button(b2); b2.pack(side="right", padx=(0,8))

    def _batch_rename_add_folders(self, paths):
        """Accept only directories. Ignore files so inner files are never listed/renamed."""
        for item in paths or []:
            try:
                item=os.path.normpath(str(item).strip().strip("{}"))
            except Exception:
                continue
            if not item or not os.path.isdir(item):
                continue
            # Skip if already listed (case-insensitive on Windows)
            key=os.path.normcase(os.path.abspath(item))
            existing={os.path.normcase(os.path.abspath(x)) for x in self.rename_folders}
            if key in existing:
                continue
            self.rename_folders.append(item)
            if hasattr(self, "batch_rename_list"):
                try:
                    self.batch_rename_list.insert("end", item)
                except Exception:
                    pass

    def _batch_rename_build_plan(self):
        if hasattr(self, "batch_rename_list"):
            try:
                self.rename_folders=[self.batch_rename_list.get(i) for i in range(self.batch_rename_list.size())]
            except Exception:
                pass
        folders=[f for f in self.rename_folders if os.path.isdir(f)]
        if not folders:
            raise ValueError("フォルダーを追加してください。" if self.lang=="ja" else "Add folders first.")
        base=self._safe_folder_name(self.rename_prefix.get())
        if not base:
            raise ValueError("共通名を入力してください。" if self.lang=="ja" else "Enter a base name.")
        try:
            start=int(str(self.rename_start.get()).strip())
            digits=max(1, min(4, int(str(self.rename_digits.get()).strip() or "2")))
        except Exception:
            raise ValueError("開始番号と桁数を確認してください。" if self.lang=="ja" else "Check start number and digits.")
        plan=[]
        seen=set()
        for i, src in enumerate(folders):
            src_p=Path(src)
            number=str(start+i).zfill(digits)
            dst=src_p.with_name(f"{base}{number}")
            key=os.path.normcase(os.path.abspath(str(dst)))
            if key in seen:
                raise ValueError(f"同じ名前が重複します: {dst.name}" if self.lang=="ja" else f"Duplicate target name: {dst.name}")
            seen.add(key)
            plan.append((src_p, dst))
        source_keys={os.path.normcase(os.path.abspath(str(s))) for s,_ in plan}
        for src, dst in plan:
            dst_key=os.path.normcase(os.path.abspath(str(dst)))
            src_key=os.path.normcase(os.path.abspath(str(src)))
            if dst.exists() and dst_key != src_key and dst_key not in source_keys:
                raise ValueError(f"同じ名前のフォルダーが既にあります:\n{dst}" if self.lang=="ja" else f"Target already exists:\n{dst}")
        return plan

    def _batch_rename_preview(self):
        try:
            plan=self._batch_rename_build_plan()
        except Exception as e:
            return messagebox.showwarning(APP_NAME, str(e))
        lines=[f"{src.name}  →  {dst.name}" for src,dst in plan[:12]]
        if len(plan)>12:
            lines.append(f"... +{len(plan)-12}")
        messagebox.showinfo(
            APP_NAME,
            (("プレビュー（フォルダー名のみ・中のファイルは変更しません）:\n\n" if self.lang=="ja"
              else "Preview (folder names only — files inside untouched):\n\n") + "\n".join(lines))
        )

    def _batch_rename_apply(self):
        try:
            plan=self._batch_rename_build_plan()
        except Exception as e:
            return messagebox.showwarning(APP_NAME, str(e))
        preview="\n".join(f"{src.name}  →  {dst.name}" for src,dst in plan[:8])
        if len(plan)>8:
            preview += f"\n... +{len(plan)-8}"
        if not messagebox.askyesno(
            APP_NAME,
            (("次のようにフォルダー名だけ変更します。\n中のファイル名は変更しません。\n\n" if self.lang=="ja"
              else "Rename folder names only.\nFiles inside will not be renamed.\n\n") + preview)
        ):
            return
        try:
            renamed=self._two_stage_rename_paths(plan)
            self.rename_folders=renamed
            if hasattr(self, "batch_rename_list"):
                self.batch_rename_list.delete(0, "end")
                for f in self.rename_folders:
                    self.batch_rename_list.insert("end", f)
            messagebox.showinfo(
                APP_NAME,
                f"{len(renamed)} 件のフォルダー名を変更しました。" if self.lang=="ja" else f"Renamed {len(renamed)} folders."
            )
        except Exception as e:
            messagebox.showerror(APP_NAME, ("名前変更に失敗しました:\n" if self.lang=="ja" else "Rename failed:\n")+str(e))


    def page_inner_file_rename(self):
        """Rename files inside folders. Folder names themselves are not changed."""
        p=self.p()
        top=self.card(self.content); top.pack(fill="x", pady=(0,12))
        hdr=tk.Frame(top, bg=p["panel"]); hdr.pack(fill="x", padx=18, pady=14)
        tk.Label(hdr, text=("フォルダー内ファイル名" if self.lang=="ja" else "Files Inside Folder"),
                 font=("Segoe UI",16,"bold"), bg=p["panel"], fg=p["text"]).pack(side="left")
        tk.Label(hdr, text=("フォルダーを指定 → 中のファイル名だけ連番変更（フォルダー名はそのまま）" if self.lang=="ja"
                            else "Pick folders → rename files inside only (folder names stay)"),
                 font=("Segoe UI",9), bg=p["panel"], fg=p["muted"]).pack(side="left", padx=12)

        def add_folder():
            folder=filedialog.askdirectory(title=("フォルダーを選択" if self.lang=="ja" else "Choose folder"))
            if folder:
                self._inner_rename_add([folder])
        def add_files():
            fs=filedialog.askopenfilenames(title=("ファイルを追加" if self.lang=="ja" else "Add files"))
            if fs:
                self._inner_rename_add(list(fs))
        def remove_sel():
            if not hasattr(self, "inner_rename_list"):
                return
            for i in reversed(self.inner_rename_list.curselection()):
                try:
                    self.inner_files.pop(i)
                except Exception:
                    pass
                self.inner_rename_list.delete(i)
        def clear_all():
            self.inner_files.clear()
            if hasattr(self, "inner_rename_list"):
                self.inner_rename_list.delete(0, "end")
        def reload_from_folders():
            # Re-scan listed folders after toggling subfolder option
            folders=set()
            for f in list(self.inner_files):
                parent=str(Path(f).parent)
                if os.path.isdir(parent):
                    folders.add(parent)
            # Also keep any paths that were folders dropped but somehow empty
            self.inner_files.clear()
            if hasattr(self, "inner_rename_list"):
                self.inner_rename_list.delete(0, "end")
            if folders:
                self._inner_rename_add(sorted(folders))

        for txt, cmd, primary in [
            (("+ フォルダー" if self.lang=="ja" else "+ Folder"), add_folder, True),
            (("+ ファイル" if self.lang=="ja" else "+ Files"), add_files, False),
            (("選択削除" if self.lang=="ja" else "Remove"), remove_sel, False),
            (("全消去" if self.lang=="ja" else "Clear"), clear_all, False),
        ]:
            b=ctk.CTkButton(hdr, text=txt, command=cmd); self.style_button(b, primary)
            b.pack(side="right", padx=(8,0))

        body=self.card(self.content); body.pack(fill="both", expand=True)

        opts=tk.Frame(body, bg=p["panel"]); opts.pack(fill="x", padx=16, pady=(14,8))
        def on_sub_toggle():
            # When toggled, user should re-add folders; soft hint only
            pass
        ctk.CTkCheckBox(
            opts,
            text=("サブフォルダー内のファイルも含める" if self.lang=="ja" else "Include files in subfolders"),
            variable=self.inner_include_subfolders, onvalue=True, offvalue=False,
            command=on_sub_toggle
        ).pack(side="left")
        tk.Label(opts, text=("※フォルダー追加 / D&D 時に適用。フォルダー名自体は変更しません。" if self.lang=="ja"
                             else "* Applied when adding / dropping folders. Folder names are not changed."),
                 bg=p["panel"], fg=p["muted"], font=("Segoe UI",9)).pack(side="left", padx=10)

        pattern=tk.Frame(body, bg=p["panel2"]); pattern.pack(fill="x", padx=16, pady=(0,10))
        tk.Label(pattern, text=("共通名" if self.lang=="ja" else "Base name"),
                 bg=p["panel2"], fg=p["text"], font=("Segoe UI",10,"bold")).pack(side="left", padx=(12,6), pady=10)
        tk.Entry(pattern, textvariable=self.inner_prefix, relief="flat", bd=0, width=28,
                 bg=p["entry"], fg=p["text"], insertbackground=p["text"]).pack(side="left", ipady=6)
        tk.Label(pattern, text=("開始" if self.lang=="ja" else "Start"),
                 bg=p["panel2"], fg=p["text"]).pack(side="left", padx=(12,4))
        tk.Entry(pattern, textvariable=self.inner_start, relief="flat", bd=0, width=6,
                 bg=p["entry"], fg=p["text"], insertbackground=p["text"]).pack(side="left", ipady=6)
        tk.Label(pattern, text=("桁数" if self.lang=="ja" else "Digits"),
                 bg=p["panel2"], fg=p["text"]).pack(side="left", padx=(12,4))
        ttk.Combobox(pattern, textvariable=self.inner_digits, state="readonly",
                     values=["1","2","3","4"], width=4).pack(side="left")
        tk.Label(pattern,
                 text=("例: TRACK + 01 → TRACK01.mp3（拡張子は維持）" if self.lang=="ja"
                       else "e.g. TRACK + 01 → TRACK01.mp3 (extension kept)"),
                 bg=p["panel2"], fg=p["muted"], font=("Segoe UI",9)).pack(side="left", padx=12)

        drop_hint=tk.Label(
            body,
            text=("ここにフォルダー（またはファイル）をドラッグ＆ドロップ" if self.lang=="ja"
                  else "Drag & drop folders (or files) here"),
            bg=p["panel"], fg=p["muted"], font=("Segoe UI",9,"bold")
        )
        drop_hint.pack(anchor="w", padx=16, pady=(0,4))

        self.inner_rename_list=tk.Listbox(
            body, selectmode="extended", relief="flat", bd=0, highlightthickness=0,
            font=("Segoe UI",10), bg=p["panel2"], fg=p["text"], selectbackground=p["accent"]
        )
        self.inner_rename_list.pack(fill="both", expand=True, padx=16, pady=(0,12))
        for f in self.inner_files:
            self.inner_rename_list.insert("end", f)
        self._enable_drop(self.inner_rename_list, self._inner_rename_add)

        foot=tk.Frame(body, bg=p["panel"]); foot.pack(fill="x", padx=16, pady=(0,16))
        b=ctk.CTkButton(foot, text=("ファイル名を一括変更" if self.lang=="ja" else "Rename Files"),
                        command=self._inner_rename_apply)
        self.style_button(b, True); b.pack(side="right")
        b2=ctk.CTkButton(foot, text=("プレビュー" if self.lang=="ja" else "Preview"),
                         command=self._inner_rename_preview)
        self.style_button(b2); b2.pack(side="right", padx=(0,8))

    def _inner_rename_add(self, paths):
        """Add files, or expand folders into files (optionally recursive). Never renames folders."""
        include=bool(self.inner_include_subfolders.get()) if hasattr(self, "inner_include_subfolders") else False
        found=[]
        for item in paths or []:
            try:
                item=os.path.normpath(str(item).strip().strip("{}"))
            except Exception:
                continue
            if not item:
                continue
            if os.path.isdir(item):
                if include:
                    for root, dirs, files in os.walk(item):
                        dirs.sort()
                        for name in sorted(files):
                            found.append(os.path.join(root, name))
                else:
                    try:
                        names=sorted(os.listdir(item))
                    except Exception:
                        names=[]
                    for name in names:
                        fp=os.path.join(item, name)
                        if os.path.isfile(fp):
                            found.append(fp)
            elif os.path.isfile(item):
                found.append(item)
        for f in found:
            key=os.path.normcase(os.path.abspath(f))
            existing={os.path.normcase(os.path.abspath(x)) for x in self.inner_files}
            if key in existing:
                continue
            self.inner_files.append(f)
            if hasattr(self, "inner_rename_list"):
                try:
                    self.inner_rename_list.insert("end", f)
                except Exception:
                    pass

    def _safe_file_stem(self, name):
        name=str(name or "").strip()
        name=re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", name)
        name=name.rstrip(" .")
        return name

    def _inner_rename_build_plan(self):
        if hasattr(self, "inner_rename_list"):
            try:
                self.inner_files=[self.inner_rename_list.get(i) for i in range(self.inner_rename_list.size())]
            except Exception:
                pass
        files=[f for f in self.inner_files if os.path.isfile(f)]
        if not files:
            raise ValueError("ファイルを追加してください（フォルダーをドロップすると中のファイルが入ります）。"
                             if self.lang=="ja" else "Add files (drop a folder to load files inside).")
        base=self._safe_file_stem(self.inner_prefix.get())
        if not base:
            raise ValueError("共通名を入力してください。" if self.lang=="ja" else "Enter a base name.")
        try:
            start=int(str(self.inner_start.get()).strip())
            digits=max(1, min(4, int(str(self.inner_digits.get()).strip() or "2")))
        except Exception:
            raise ValueError("開始番号と桁数を確認してください。" if self.lang=="ja" else "Check start number and digits.")
        plan=[]
        seen=set()
        for i, src in enumerate(files):
            src_p=Path(src)
            number=str(start+i).zfill(digits)
            dst=src_p.with_name(f"{base}{number}{src_p.suffix}")
            key=os.path.normcase(os.path.abspath(str(dst)))
            if key in seen:
                raise ValueError(f"同じ名前が重複します: {dst.name}" if self.lang=="ja" else f"Duplicate target: {dst.name}")
            seen.add(key)
            plan.append((src_p, dst))
        source_keys={os.path.normcase(os.path.abspath(str(s))) for s,_ in plan}
        for src, dst in plan:
            dst_key=os.path.normcase(os.path.abspath(str(dst)))
            src_key=os.path.normcase(os.path.abspath(str(src)))
            if dst.exists() and dst_key != src_key and dst_key not in source_keys:
                raise ValueError(f"同じ名前のファイルが既にあります:\n{dst}" if self.lang=="ja" else f"Target already exists:\n{dst}")
        return plan

    def _inner_rename_preview(self):
        try:
            plan=self._inner_rename_build_plan()
        except Exception as e:
            return messagebox.showwarning(APP_NAME, str(e))
        lines=[f"{src.name}  →  {dst.name}" for src,dst in plan[:12]]
        if len(plan)>12:
            lines.append(f"... +{len(plan)-12}")
        messagebox.showinfo(
            APP_NAME,
            (("プレビュー（ファイル名のみ・フォルダー名は変更しません）:\n\n" if self.lang=="ja"
              else "Preview (file names only — folder names unchanged):\n\n") + "\n".join(lines))
        )

    def _inner_rename_apply(self):
        try:
            plan=self._inner_rename_build_plan()
        except Exception as e:
            return messagebox.showwarning(APP_NAME, str(e))
        preview="\n".join(f"{src.name}  →  {dst.name}" for src,dst in plan[:8])
        if len(plan)>8:
            preview += f"\n... +{len(plan)-8}"
        if not messagebox.askyesno(
            APP_NAME,
            (("次のようにファイル名を変更します。\nフォルダー名は変更しません。\n\n" if self.lang=="ja"
              else "Rename files as follows.\nFolder names will not change.\n\n") + preview)
        ):
            return
        try:
            renamed=self._two_stage_rename_paths(plan)
            self.inner_files=renamed
            if hasattr(self, "inner_rename_list"):
                self.inner_rename_list.delete(0, "end")
                for f in self.inner_files:
                    self.inner_rename_list.insert("end", f)
            messagebox.showinfo(
                APP_NAME,
                f"{len(renamed)} 件のファイル名を変更しました。" if self.lang=="ja" else f"Renamed {len(renamed)} files."
            )
        except Exception as e:
            messagebox.showerror(APP_NAME, ("名前変更に失敗しました:\n" if self.lang=="ja" else "Rename failed:\n")+str(e))

    def open_batch_tags(self,event=None):
        # Ctrl+K should open the editor inside the main window, not in a Toplevel.
        if event is not None:
            self.show_page("batch")
            return "break"

        p=self.p()
        win=self.content

        tk.Label(win,text=self.tr("batch_title"),font=("Segoe UI",18,"bold"),
                 bg=p["bg"],fg=p["text"]).pack(anchor="w",padx=20,pady=(16,8))

        # Fixed footer: stays visible even when the window is not maximized.
        footer=tk.Frame(win,bg=p["bg"])
        footer.pack(side="bottom",fill="x",padx=20,pady=(0,14))

        footer_hint=tk.Label(
            footer,
            text=("Ctrl+S でも保存できます" if self.lang=="ja" else "Ctrl+S also saves"),
            bg=p["bg"],fg=p["muted"],font=("Segoe UI",9)
        )
        footer_hint.pack(side="left")

        panel=self.card(win)
        panel.pack(fill="both",expand=True,padx=20,pady=(0,18))

        # Track controls are deliberately at the TOP so they stay visible even on a smaller window.
        trackbox=tk.Frame(panel,bg=p["panel2"])
        trackbox.pack(fill="x",padx=14,pady=(14,8))

        auto=self.batch_auto
        tk.Checkbutton(trackbox,text=self.tr("auto_track"),variable=auto,
                       bg=p["panel2"],fg=p["text"],selectcolor=p["entry"],
                       font=("Segoe UI",10,"bold")).pack(side="left",padx=(12,16),pady=10)

        tk.Label(trackbox,text=self.tr("track_range"),bg=p["panel2"],fg=p["text"],
                 font=("Segoe UI",10,"bold")).pack(side="left")
        track_range=self.batch_track_range
        track_entry=tk.Entry(trackbox,textvariable=track_range,width=18,font=("Segoe UI",12,"bold"),
                             relief="flat",bd=0,bg=p["entry"],fg=p["text"],insertbackground=p["text"])
        track_entry.pack(side="left",padx=(10,10),ipady=7)
        tk.Label(trackbox,text=("例: 50 または 50-60" if self.lang=="ja" else "e.g. 50 or 50-60"),
                 bg=p["panel2"],fg=p["muted"],font=("Segoe UI",9)).pack(side="left")

        # Two-column metadata layout keeps the window usable without maximizing.
        form=tk.Frame(panel,bg=p["panel"])
        form.pack(fill="x",padx=14,pady=6)
        form.grid_columnconfigure(1,weight=1)
        form.grid_columnconfigure(3,weight=1)

        fields=[
            (self.tr("title_common"),"title"),
            (self.tr("artist"),"artist"),
            (self.tr("album"),"album"),
            (self.tr("album_artist"),"album_artist"),
            (self.tr("date"),"date"),
            (self.tr("genre"),"genre"),
            (self.tr("disc"),"disc"),
            (self.tr("comment"),"comment")
        ]
        vs=self.batch_tagvars
        for i,(lab,k) in enumerate(fields):
            r=i//2; pair=i%2
            lc=pair*2; ec=lc+1
            tk.Label(form,text=lab,bg=p["panel"],fg=p["text"]).grid(
                row=r,column=lc,sticky="w",pady=5,padx=(0 if pair==0 else 18,8))
            tk.Entry(form,textvariable=vs[k],relief="flat",bd=0,
                     bg=p["entry"],fg=p["text"],insertbackground=p["text"]).grid(
                row=r,column=ec,sticky="ew",pady=5,ipady=7)

        optionrow=tk.Frame(panel,bg=p["panel"])
        optionrow.pack(fill="x",padx=14,pady=(4,8))
        use_filename=self.batch_use_filename
        tk.Checkbutton(optionrow,text=self.tr("filename_title"),variable=use_filename,
                       bg=p["panel"],fg=p["text"],selectcolor=p["entry"]).pack(side="left")

        # Batch file-name editor. This changes file names only, not metadata.
        renamebox=tk.Frame(panel,bg=p["panel2"])
        renamebox.pack(fill="x",padx=14,pady=(0,8))
        rename_prefix=self.batch_rename_prefix
        rename_start=self.batch_rename_start
        rename_digits=self.batch_rename_digits

        tk.Label(renamebox,text=("一括名前編集（保存 / 適用でも保存されます）" if self.lang=="ja" else "Batch rename (also saved by Save / Apply)"),
                 bg=p["panel2"],fg=p["text"],font=("Segoe UI",10,"bold")).grid(
                     row=0,column=0,sticky="w",padx=(12,8),pady=8)
        tk.Label(renamebox,text=("名前" if self.lang=="ja" else "Name"),
                 bg=p["panel2"],fg=p["text"]).grid(row=0,column=1,sticky="e",padx=(4,4))
        tk.Entry(renamebox,textvariable=rename_prefix,width=24,relief="flat",bd=0,
                 bg=p["entry"],fg=p["text"],insertbackground=p["text"]).grid(
                     row=0,column=2,sticky="ew",ipady=6,padx=(0,8))
        tk.Label(renamebox,text=("開始番号" if self.lang=="ja" else "Start"),
                 bg=p["panel2"],fg=p["text"]).grid(row=0,column=3,sticky="e",padx=(4,4))
        tk.Entry(renamebox,textvariable=rename_start,width=6,relief="flat",bd=0,
                 bg=p["entry"],fg=p["text"],insertbackground=p["text"]).grid(
                     row=0,column=4,ipady=6,padx=(0,8))
        tk.Label(renamebox,text=("桁数" if self.lang=="ja" else "Digits"),
                 bg=p["panel2"],fg=p["text"]).grid(row=0,column=5,sticky="e",padx=(4,4))
        ttk.Combobox(renamebox,textvariable=rename_digits,state="readonly",
                     values=["1","2","3","4"],width=4).grid(row=0,column=6,padx=(0,8))
        renamebox.grid_columnconfigure(2,weight=1)

        tk.Label(renamebox,
                 text=("例: 名前=TRACK / 開始=1 / 桁数=2 → TRACK01.mp3, TRACK02.mp3"
                       if self.lang=="ja" else
                       "Example: Name=TRACK / Start=1 / Digits=2 → TRACK01.mp3, TRACK02.mp3"),
                 bg=p["panel2"],fg=p["muted"],font=("Segoe UI",9)).grid(
                     row=1,column=0,columnspan=7,sticky="w",padx=12,pady=(0,8))

        # Batch cover art
        coverrow=tk.Frame(panel,bg=p["panel2"])
        coverrow.pack(fill="x",padx=14,pady=(0,8))
        batch_cover=self.batch_cover

        tk.Label(
            coverrow,
            text=self.tr("cover"),
            bg=p["panel2"],
            fg=p["text"],
            font=("Segoe UI",10,"bold")
        ).pack(side="left",padx=(12,8),pady=10)

        cover_entry=tk.Entry(
            coverrow,
            textvariable=batch_cover,
            state="readonly",
            relief="flat",
            bd=0,
            bg=p["entry"],
            fg=p["text"],
            readonlybackground=p["entry"]
        )
        cover_entry.pack(side="left",fill="x",expand=True,ipady=6)

        def choose_batch_cover():
            f=filedialog.askopenfilename(
                parent=self.root,
                filetypes=[
                    ("Image","*.jpg *.jpeg *.png *.webp *.bmp"),
                    ("JPEG","*.jpg *.jpeg"),
                    ("PNG","*.png"),
                    ("All","*.*")
                ]
            )
            if f:
                batch_cover.set(f)
                try:
                    from PIL import Image, ImageTk
                    im=Image.open(f)
                    im.thumbnail((110,110))
                    ph=ImageTk.PhotoImage(im)
                    cover_preview.configure(image=ph,text="")
                    cover_preview.image=ph
                except Exception:
                    cover_preview.configure(image="",text=os.path.basename(f))
                    cover_preview.image=None
                try:
                    footer_hint.config(
                        text=("選択中のカバー: "+os.path.basename(f)) if self.lang=="ja"
                        else ("Selected cover: "+os.path.basename(f))
                    )
                except Exception:
                    pass

        def clear_batch_cover():
            batch_cover.set("")
            try:
                cover_preview.configure(
                    image="",
                    text=("カバー未選択" if self.lang=="ja" else "No cover selected")
                )
                cover_preview.image=None
                footer_hint.config(text=("Ctrl+S でも保存できます" if self.lang=="ja" else "Ctrl+S also saves"))
            except Exception:
                pass

        bc=ctk.CTkButton(coverrow,text=self.tr("cover_choose"),command=choose_batch_cover)
        self.style_button(bc)
        bc.pack(side="left",padx=8)

        br=ctk.CTkButton(coverrow,text=self.tr("clear"),command=clear_batch_cover)
        self.style_button(br)
        br.pack(side="left",padx=(0,8))

        previewrow=tk.Frame(panel,bg=p["panel"])
        previewrow.pack(fill="x",padx=14,pady=(0,6))
        cover_preview=tk.Label(
            previewrow,
            text=("カバー未選択" if self.lang=="ja" else "No cover selected"),
            bg=p["panel2"],fg=p["muted"],width=18,height=5
        )
        cover_preview.pack(side="left")

        tk.Label(
            panel,
            text=("選んだ画像を対応ファイルすべてのカバー画像として設定します（MP3 / M4A / FLAC / MP4）。"
                  if self.lang=="ja"
                  else "The selected image will be applied as cover art to all supported files (MP3 / M4A / FLAC / MP4)."),
            bg=p["panel"],
            fg=p["muted"],
            font=("Segoe UI",9)
        ).pack(anchor="w",padx=14,pady=(0,6))

        # File list: drag files directly here.
        tk.Label(panel,text=self.tr("drop_files"),bg=p["panel"],fg=p["muted"],
                 font=("Segoe UI",9,"bold")).pack(anchor="w",padx=14,pady=(2,4))
        fileframe=tk.Frame(panel,bg=p["panel"],height=230)
        fileframe.pack(fill="both",expand=True,padx=14,pady=(0,8))
        fileframe.pack_propagate(False)

        self.batch_listbox=tk.Listbox(fileframe,selectmode="extended",relief="flat",bd=0,
                                      highlightthickness=0,font=("Segoe UI",10),height=11,
                                      bg=p["panel2"],fg=p["text"],selectbackground=p["accent"])
        self.batch_listbox.pack(side="left",fill="both",expand=True)
        sb=tk.Scrollbar(fileframe,command=self.batch_listbox.yview)
        sb.pack(side="right",fill="y")
        self.batch_listbox.configure(yscrollcommand=sb.set)

        for f in self.batch_files:
            self.batch_listbox.insert("end",f)
        self._enable_drop(self.batch_listbox,self._add_batch_dropped)
        self._enable_drop(fileframe,self._add_batch_dropped)

        buttons=tk.Frame(panel,bg=p["panel"])
        buttons.pack(fill="x",padx=14,pady=(0,14))

        supported_batch_exts={".mp3",".m4a",".wav",".aac",".adts",".flac",".mp4",".mkv",".webm",".mov",".at3"}

        def add_more():
            fs=list(filedialog.askopenfilenames(
                parent=self.root,
                filetypes=[("Audio / Video","*.mp3 *.m4a *.wav *.aac *.adts *.flac *.mp4 *.mkv *.webm *.mov *.at3"),
                           ("All","*.*")]
            ))
            self._add_batch_dropped(fs)

        def add_folder():
            folder=filedialog.askdirectory(
                parent=self.root,
                title=("タグ編集するフォルダーを選択" if self.lang=="ja" else "Choose a folder to tag")
            )
            if not folder:
                return
            found=[]
            try:
                for root,dirs,files in os.walk(folder):
                    for name in files:
                        path=os.path.join(root,name)
                        if os.path.splitext(name)[1].lower() in supported_batch_exts:
                            found.append(path)
            except Exception as e:
                return messagebox.showerror(APP_NAME,str(e),parent=self.root)
            found.sort(key=lambda x:x.lower())
            if not found:
                return messagebox.showwarning(
                    APP_NAME,
                    ("対応する音声・動画ファイルが見つかりませんでした。" if self.lang=="ja" else "No supported audio/video files were found."),
                    parent=self.root
                )
            self._add_batch_dropped(found)

        def remove_selected_batch():
            sel=list(self.batch_listbox.curselection())
            if not sel:return
            for i in reversed(sel):
                self.batch_files.pop(i)
            self.batch_listbox.delete(0,"end")
            for f in self.batch_files:self.batch_listbox.insert("end",f)

        def clear_all_batch():
            self.batch_files=[]
            try:self.batch_listbox.delete(0,"end")
            except Exception:pass

        b=ctk.CTkButton(buttons,text=("+ ファイル追加" if self.lang=="ja" else "+ Add files"),command=add_more);self.style_button(b);b.pack(side="left")
        b=ctk.CTkButton(buttons,text=("📁 フォルダー追加" if self.lang=="ja" else "📁 Add folder"),command=add_folder);self.style_button(b);b.pack(side="left",padx=8)
        b=ctk.CTkButton(buttons,text=("選択した項目を消去" if self.lang=="ja" else "Remove selected"),command=remove_selected_batch);self.style_button(b);b.pack(side="left",padx=(0,8))
        b=ctk.CTkButton(buttons,text=("全消去" if self.lang=="ja" else "Clear all"),command=clear_all_batch);self.style_button(b);b.pack(side="left")

        def parse_track_numbers(text,count):
            text=text.strip()
            if not text:
                return list(range(1,count+1))
            if "-" in text:
                a,b=text.split("-",1)
                first=int(a.strip()); last=int(b.strip())
                if last < first:
                    raise ValueError("終了番号は開始番号以上にしてください。" if self.lang=="ja"
                                     else "End number must be greater than or equal to start number.")
                nums=list(range(first,last+1))
                if len(nums) < count:
                    raise ValueError("ファイル数が範囲を超えています。範囲を広げてください。" if self.lang=="ja"
                                     else "There are more files than numbers in the range.")
                return nums[:count]
            first=int(text)
            return list(range(first,first+count))

        def reset_batch_tag_editor_fields():
            # Reset editor controls after an edit operation finishes.
            try:
                for var in vs.values():
                    var.set("")
                use_filename.set(False)
                auto.set(False)
                track_range.set("1")
                rename_prefix.set("")
                rename_start.set("1")
                rename_digits.set("2")
                batch_cover.set("")
                cover_preview.configure(
                    image="",
                    text=("カバー未選択" if self.lang=="ja" else "No cover selected")
                )
                cover_preview.image=None
            except Exception:
                pass

        def apply():
            current=list(self.batch_files)
            if not current:
                return messagebox.showwarning(APP_NAME,self.tr("need_files"),parent=self.root)
            ff=tool("ffmpeg")
            has_normal_tag_changes=any(v.get() for v in vs.values()) or use_filename.get() or auto.get()
            if has_normal_tag_changes and not ff:
                return messagebox.showerror(APP_NAME,self.tr("ffmpeg"),parent=self.root)
            try:
                nums=parse_track_numbers(track_range.get(),len(current)) if auto.get() else None
            except Exception as e:
                return messagebox.showerror(APP_NAME,str(e),parent=self.root)

            # Snapshot Tk values on the UI thread. Never read Tk variables from the worker.
            tag_values={k:v.get() for k,v in vs.items()}
            use_filename_value=bool(use_filename.get())
            auto_value=bool(auto.get())
            cover=batch_cover.get().strip() or None
            rename_requested=bool(rename_prefix.get().strip())

            # Keep the UI responsive while FFmpeg/mutagen processes the files.
            try:
                save_btn.configure(state="disabled",text=("保存中..." if self.lang=="ja" else "Saving..."))
                rename_btn.configure(state="disabled")
                cover_btn.configure(state="disabled")
                footer_hint.config(text=(f"0/{len(current)} 処理中" if self.lang=="ja" else f"0/{len(current)} processing"))
            except Exception:
                pass

            def worker():
                failures=[]
                next_track_index=0
                for i,path in enumerate(current,1):
                    try:
                        tags={k:v for k,v in tag_values.items() if v}
                        if use_filename_value:
                            tags["title"]=os.path.splitext(os.path.basename(path))[0]
                        if auto_value:
                            # A failed file must not consume a track number.
                            # The next successful file receives the same pending number.
                            tags["track"]=str(nums[next_track_index])
                        if cover and not tags:
                            _replace_cover_art(path,cover)
                        elif tags or cover:
                            write_tags_with_cover(ff,path,tags,cover_path=cover)

                        if auto_value:
                            next_track_index += 1
                    except Exception as e:
                        failures.append(f"{os.path.basename(path)}: {e}")
                    try:
                        self.root.after(0,lambda done=i,total=len(current): footer_hint.config(
                            text=(f"{done}/{total} 処理中" if self.lang=="ja" else f"{done}/{total} processing")
                        ))
                    except Exception:
                        pass

                def finish():
                    try:
                        save_btn.configure(state="normal",text=("💾 保存 / 適用" if self.lang=="ja" else "💾 Save / Apply"))
                        rename_btn.configure(state="normal")
                        cover_btn.configure(state="normal")
                        footer_hint.config(text=("Ctrl+S でも保存できます" if self.lang=="ja" else "Ctrl+S also saves"))
                    except Exception:
                        pass

                    # Keep only failed files in the drop list. If everything succeeded,
                    # return the drop area to its empty state for the next batch.
                    failed_names={line.split(":",1)[0] for line in failures}
                    failed_paths=[p for p in current if os.path.basename(p) in failed_names]

                    if failures:
                        self.batch_files=failed_paths
                        try:
                            self.batch_listbox.delete(0,"end")
                            for f in self.batch_files:
                                self.batch_listbox.insert("end",f)
                        except Exception:
                            pass
                        reset_batch_tag_editor_fields()
                        messagebox.showwarning(
                            APP_NAME,
                            (f"{len(current)-len(failures)}/{len(current)} 件 保存しました。\n成功したファイルは一覧から消しました。\n\n失敗:\n"
                             if self.lang=="ja" else
                             f"Saved {len(current)-len(failures)}/{len(current)} files.\nSuccessful files were removed from the list.\n\nFailed:\n")
                            + "\n".join(failures[:8]),
                            parent=self.root
                        )
                        return

                    # File renaming is fast and may show confirmation dialogs, so keep it on Tk thread.
                    if rename_requested:
                        renamed_ok=apply_batch_rename(confirm=False, close_after=False)
                        if not renamed_ok:
                            return
                        self.batch_files=[]
                        try:self.batch_listbox.delete(0,"end")
                        except Exception:pass
                        reset_batch_tag_editor_fields()
                        messagebox.showinfo(
                            APP_NAME,
                            ("タグ・トラック番号・ファイル名をまとめて保存しました。\n一覧をクリアしました。"
                             if self.lang=="ja" else
                             "Saved tags, track numbers, and file names together.\nThe list was cleared."),
                            parent=self.root
                        )
                    else:
                        self.batch_files=[]
                        try:self.batch_listbox.delete(0,"end")
                        except Exception:pass
                        reset_batch_tag_editor_fields()
                        messagebox.showinfo(APP_NAME,self.tr("batch_done"),parent=self.root)

                try:
                    self.root.after(0,finish)
                except Exception:
                    pass

            threading.Thread(target=worker,daemon=True).start()

        def apply_batch_rename(confirm=True, close_after=False):
            current=list(self.batch_files)
            if not current:
                return messagebox.showwarning(APP_NAME,self.tr("need_files"),parent=self.root)

            base=rename_prefix.get().strip()
            if not base:
                return messagebox.showwarning(
                    APP_NAME,
                    "新しい名前を入力してください。" if self.lang=="ja" else "Enter a new file name.",
                    parent=self.root
                )
            # Windows-invalid filename characters are replaced instead of causing a partial rename.
            safe_base=re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", base).strip().rstrip(". ")
            if not safe_base:
                return messagebox.showwarning(APP_NAME,"有効な名前を入力してください。",parent=self.root)
            try:
                start=int(rename_start.get().strip())
                digits=max(1,min(4,int(rename_digits.get())))
            except Exception:
                return messagebox.showerror(APP_NAME,"開始番号と桁数を確認してください。",parent=self.root)

            plan=[]
            seen=set()
            for i,path in enumerate(current):
                src=Path(path)
                number=str(start+i).zfill(digits)
                dst=src.with_name(f"{safe_base}{number}{src.suffix}")
                key=os.path.normcase(os.path.abspath(str(dst)))
                if key in seen:
                    return messagebox.showerror(APP_NAME,f"同じ名前が重複します:\n{dst.name}",parent=self.root)
                seen.add(key)
                plan.append((src,dst))

            source_keys={os.path.normcase(os.path.abspath(str(src))) for src,_ in plan}
            for src,dst in plan:
                dst_key=os.path.normcase(os.path.abspath(str(dst)))
                src_key=os.path.normcase(os.path.abspath(str(src)))
                if dst.exists() and dst_key != src_key and dst_key not in source_keys:
                    return messagebox.showerror(
                        APP_NAME,
                        f"同じ名前のファイルが既にあります:\n{dst}",
                        parent=self.root
                    )

            preview="\n".join(f"{src.name}  →  {dst.name}" for src,dst in plan[:8])
            if len(plan)>8:
                preview += f"\n... +{len(plan)-8} 件"
            if confirm:
                if not messagebox.askyesno(
                    APP_NAME,
                    ("次のようにファイル名を変更します:\n\n" if self.lang=="ja"
                     else "Rename files as follows:\n\n") + preview,
                    parent=self.root
                ):
                    return False

            # Two-stage rename prevents A->B / B->C collisions.
            temp_plan=[]
            try:
                for idx,(src,dst) in enumerate(plan):
                    if os.path.normcase(os.path.abspath(str(src))) == os.path.normcase(os.path.abspath(str(dst))):
                        temp_plan.append((src,src,dst))
                        continue
                    tmp=src.with_name(f".__atrac_rename_{uuid.uuid4().hex}_{idx}{src.suffix}")
                    src.rename(tmp)
                    temp_plan.append((src,tmp,dst))

                renamed=[]
                for original,tmp,dst in temp_plan:
                    if tmp != original or dst != original:
                        tmp.rename(dst)
                    renamed.append(str(dst))
                self.batch_files=[]
                self.batch_listbox.delete(0,"end")
                reset_batch_tag_editor_fields()
                if confirm:
                    messagebox.showinfo(
                        APP_NAME,
                        (f"{len(renamed)} 件のファイル名を変更しました。\n一覧をクリアしました。" if self.lang=="ja"
                         else f"Renamed {len(renamed)} files.\nThe list was cleared."),
                        parent=self.root
                    )
                if close_after:
                    self.show_page("home")
                return True
            except Exception as e:
                # Best-effort rollback for files still at temporary names.
                for original,tmp,dst in reversed(temp_plan):
                    try:
                        if tmp.exists() and not original.exists():
                            tmp.rename(original)
                        elif dst.exists() and not original.exists():
                            dst.rename(original)
                    except Exception:
                        pass
                self.batch_files=[str(p) for p in current]
                self.batch_listbox.delete(0,"end")
                for f in self.batch_files:
                    self.batch_listbox.insert("end",f)
                messagebox.showerror(
                    APP_NAME,
                    ("名前変更に失敗しました:\n" if self.lang=="ja" else "Rename failed:\n")+str(e),
                    parent=self.root
                )
                return False

        def apply_cover_only():
            current=list(self.batch_files)
            cover=batch_cover.get().strip()
            if not current:
                return messagebox.showwarning(APP_NAME,self.tr("need_files"),parent=self.root)
            if not cover:
                return messagebox.showwarning(APP_NAME,"カバー画像を選んでください。",parent=self.root)
            if not os.path.isfile(cover):
                return messagebox.showerror(APP_NAME,"カバー画像ファイルが見つかりません。",parent=self.root)

            ok=0
            failures=[]
            for path in current:
                try:
                    _replace_cover_art(path,cover)
                    ok+=1
                except Exception as e:
                    failures.append(f"{os.path.basename(path)}: {e}")

            if failures:
                failed_names={line.split(":",1)[0] for line in failures}
                self.batch_files=[p for p in current if os.path.basename(p) in failed_names]
                try:
                    self.batch_listbox.delete(0,"end")
                    for f in self.batch_files:self.batch_listbox.insert("end",f)
                except Exception:pass
                return messagebox.showwarning(
                    APP_NAME,
                    f"{ok}/{len(current)} 件 カバー画像を変更しました。\n成功したファイルは一覧から消しました。\n\n失敗:\n" + "\n".join(failures[:8]),
                    parent=self.root
                )
            self.batch_files=[]
            try:self.batch_listbox.delete(0,"end")
            except Exception:pass
            reset_batch_tag_editor_fields()
            messagebox.showinfo(APP_NAME,f"{ok} 件のカバー画像を変更しました。",parent=self.root)

        rename_btn=ctk.CTkButton(
            footer,
            text=("✎ 名前だけ一括保存" if self.lang=="ja" else "✎ Save file names only"),
            command=apply_batch_rename
        )
        self.style_button(rename_btn,True)
        rename_btn.pack(side="right",padx=(0,8))

        cover_btn=ctk.CTkButton(
            footer,
            text=("🖼 カバー画像だけ変更" if self.lang=="ja" else "🖼 Change cover only"),
            command=apply_cover_only
        )
        self.style_button(cover_btn,True)
        cover_btn.pack(side="right",padx=(0,8))

        save_text=("💾 保存 / 適用" if self.lang=="ja" else "💾 Save / Apply")
        save_btn=ctk.CTkButton(footer,text=save_text,command=apply)
        self.style_button(save_btn,True)
        save_btn.pack(side="right")

        close_text=("ホームへ戻る" if self.lang=="ja" else "Back to Home")
        close_btn=ctk.CTkButton(footer,text=close_text,command=lambda:self.show_page("home"))
        self.style_button(close_btn)
        close_btn.pack(side="right",padx=(0,8))

        self.root.bind("<Control-s>",lambda e:apply())
        track_entry.focus_set()
        return "break"

def main():
    root=(TkinterDnD.Tk() if HAS_DND else tk.Tk())
    App(root)
    try:
        _base=getattr(sys,"_MEIPASS",None) or os.path.dirname(os.path.abspath(__file__))
        _ico=os.path.join(_base,"ATRAC_v30.ico")
        if os.path.exists(_ico):
            root.iconbitmap(_ico)
    except Exception:
        pass
    root.mainloop()

if __name__=="__main__":
    main()
