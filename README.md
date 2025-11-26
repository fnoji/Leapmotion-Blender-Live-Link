
This add-on is not functioning correctly and requires fixes or review before it can be used regularly.
Pull requests (or other contributions) are welcome!

https://github.com/user-attachments/assets/4657fe5f-9b52-4fa8-b199-bbf7102106e6

# Leap Motion to Blender Live Link
[English](#english) | [日本語](#japanese)
<a name="english"></a>
## English
This project enables real-time hand tracking data streaming from an Ultraleap (Leap Motion) controller directly to Blender. It bypasses the need for intermediate software like Unity or SteamVR by using a direct Python-to-Blender UDP connection.
### Features
*   **Real-time Tracking**: Low-latency streaming of hand and finger bone data.
*   **Dual Hand Support**: Tracks both left and right hands simultaneously.
*   **Debug Visualization**: Instantly generate a debug hand rig in Blender to verify tracking.
*   **Direct API Access**: Uses the official `leapc-python-bindings` for raw data access.
*   **Blender Addon**: Simple UI panel to control the receiver and generate rigs.
### Prerequisites
*   **Hardware**: Ultraleap Leap Motion Controller (or Stereo IR 170).
*   **Software**: Ultraleap Gemini Tracking Software (installed and running).
*   **Blender**: Version 4.0 or later (Tested on 4.1).
*   **Python**: Python 3.10 or later (for the sender script).
### Installation
The project consists of two parts: the **Sender App** (Python script) and the **Blender Addon**.
#### 1. Sender App Setup
The sender app runs outside of Blender to capture Leap Motion data and send it via UDP.
1.  Clone this repository.
2.  Navigate to the `sender` directory (or root).
3.  Create a virtual environment (recommended):
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```
4.  Install dependencies:
    ```bash
    pip install -r sender/requirements.txt
    ```
    *Note: The `leapc-python-bindings` are installed directly from GitHub. You may need to ensure you have a C compiler installed if pre-built binaries are not available for your platform, or manually copy the `leapc_cffi` folder from the Leap SDK if you encounter issues.*
#### 2. Blender Addon Installation
1.  Open Blender.
2.  Go to **Edit > Preferences > Add-ons**.
3.  Click **Install...** and select the `leap_live_link.zip` file found in the `leap_blender_link` directory (or create it by zipping the `leap_live_link` folder).
4.  Enable the addon: **Animation: Leap Motion Live Link**.
### Usage
#### Step 1: Start the Sender
Run the sender script from your terminal:
```bash
python sender/sender.py
```
You should see a message: `Connected to Leap Motion Service`.
#### Step 2: Receive in Blender
1.  In Blender, press **N** to open the Sidebar.
2.  Click on the **Leap Motion Link** tab.
3.  **Generate Debug Hand**: Click this button to create a simple armature representing the hands.
4.  **Start Receiver**: Click this to start listening for data.
5.  Move your hands over the controller. The Blender rig should move in real-time.
### Troubleshooting
*   **"ModuleNotFoundError: No module named 'leap'"**: Ensure you have installed the requirements in your virtual environment. If using Python 3.12+, you might need to manually copy the `leapc_cffi` folder and `LeapC.dll` from the Ultraleap SDK installation folder (`C:\Program Files\Ultraleap\LeapSDK\leapc_cffi`) to your virtual environment's `site-packages`.
*   **Hands are flat/not moving**: Ensure you are using the latest version of the addon which includes vector-based bone alignment. Re-generate the debug hand if necessary.
*   **Connection Refused**: Check that the `IP` and `PORT` in `sender.py` match the settings in the Blender addon panel (Default: 127.0.0.1:9009).
---
<a name="japanese"></a>
## 日本語 (Japanese)
このプロジェクトは、Ultraleap (Leap Motion) コントローラーからのハンドトラッキングデータを、リアルタイムでBlenderにストリーミングすることを可能にします。UnityやSteamVRといった中間ソフトウェアを介さず、PythonからBlenderへUDPで直接通信を行います。
### 機能
*   **リアルタイムトラッキング**: 手と指のボーンデータを低遅延でストリーミングします。
*   **両手対応**: 左右の手を同時にトラッキングします。
*   **デバッグ表示**: Blender内でトラッキング確認用のデバッグ用リグ（アーマチュア）を即座に生成できます。
*   **直接APIアクセス**: 公式の `leapc-python-bindings` を使用し、生のデータにアクセスします。
*   **Blenderアドオン**: 受信の制御やリグ生成を行うためのシンプルなUIパネルを提供します。
### 必須環境
*   **ハードウェア**: Ultraleap Leap Motion Controller (または Stereo IR 170)。
*   **ソフトウェア**: Ultraleap Gemini Tracking Software (インストールおよび起動済みであること)。
*   **Blender**: バージョン 4.0 以降 (4.1で動作確認済み)。
*   **Python**: Python 3.10 以降 (送信アプリ実行用)。
### インストール
このプロジェクトは、**送信アプリ (Sender App)** と **Blenderアドオン** の2つの部分で構成されています。
#### 1. 送信アプリのセットアップ
送信アプリはBlenderの外で動作し、Leap Motionのデータを取得してUDPで送信します。
1.  このリポジトリをクローンします。
2.  `sender` ディレクトリ（またはルート）に移動します。
3.  仮想環境の作成を推奨します:
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```
4.  依存ライブラリをインストールします:
    ```bash
    pip install -r sender/requirements.txt
    ```
    *注意: `leapc-python-bindings` はGitHubから直接インストールされます。プラットフォーム用のビルド済みバイナリがない場合はCコンパイラが必要になることがあります。問題が発生した場合は、Leap SDKから `leapc_cffi` フォルダを手動でコピーする必要があるかもしれません。*
#### 2. Blenderアドオンのインストール
1.  Blenderを開きます。
2.  **編集 (Edit) > プリファレンス (Preferences) > アドオン (Add-ons)** に移動します。
3.  **インストール (Install...)** をクリックし、`leap_blender_link` ディレクトリにある `leap_live_link.zip` ファイルを選択します（もし無ければ `leap_live_link` フォルダをZIP圧縮して作成してください）。
4.  アドオン **Animation: Leap Motion Live Link** を有効化します。
### 使い方
#### ステップ 1: 送信アプリの起動
ターミナルから送信スクリプトを実行します:
```bash
python sender/sender.py
```
`Connected to Leap Motion Service` というメッセージが表示されれば成功です。
#### ステップ 2: Blenderでの受信
1.  Blenderで **N** キーを押してサイドバーを開きます。
2.  **Leap Motion Link** タブをクリックします。
3.  **Generate Debug Hand**: このボタンをクリックして、手を表すシンプルなアーマチュア（骨組み）を生成します。
4.  **Start Receiver**: このボタンをクリックして、データの受信を開始します。
5.  コントローラーの上で手を動かしてください。Blenderのリグがリアルタイムで動くはずです。
### トラブルシューティング
*   **"ModuleNotFoundError: No module named 'leap'"**: 仮想環境にライブラリが正しくインストールされているか確認してください。Python 3.12以降を使用している場合、Ultraleap SDKのインストールフォルダ (`C:\Program Files\Ultraleap\LeapSDK\leapc_cffi`) から `leapc_cffi` フォルダと `LeapC.dll` を、仮想環境の `site-packages` フォルダに手動でコピーする必要がある場合があります。
*   **手が平らになる / 動かない**: ベクトルベースのボーン整列を含む最新バージョンのアドオンを使用しているか確認してください。必要に応じてデバッグハンドを再生成してください。
*   **接続拒否 (Connection Refused)**: `sender.py` の `IP` と `PORT` の設定が、Blenderアドオンパネルの設定（デフォルト: 127.0.0.1:9009）と一致しているか確認してください。
## License
MIT
