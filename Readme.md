# TRENDVISION

TrendVision is a real-time social listening tool that analyzes Reddit trends using NLP and forecasting.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   - Go to https://www.reddit.com/prefs/apps.
   - **Note**: You may see a banner about "Responsible Builder Policy". Ignore it and scroll to the **bottom-left**.
   - Click the button **are you a developer? create an app...** (or **create another app**).
   - **Name**: `TrendVision`
   - **Select**: `script` (This is crucial!).
   - **Redirect URI**: `http://localhost:8080`
   - Click **Create app**.
   - Copy the **Client ID** (string under the name) and **Secret**.
   - Open `.env` in this project and paste them.

3. **Run the App**:
   ```bash
   streamlit run UI.py
   ```

4. **Initialize Data**:
   - Go to the **Settings** page in the sidebar.
   - Click the buttons in order: **Fetch Data** -> **Extract Keywords** -> **Analyze Sentiment** -> **Generate Forecast**.

## Troubleshooting

### Windows Long Path Error
If you see an error like `[Errno 2] No such file or directory` related to `prophet` or `stan_model` during installation:
1. Open **PowerShell** as Administrator.
2. Run this command to enable long paths:
   ```powershell
   New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
   ```
3. Restart your terminal and try `pip install -r requirements.txt` again.