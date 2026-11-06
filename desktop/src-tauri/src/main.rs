// My Personal Qur'an for Windows: the same single-file web app as on Android (index.html), in a WebView2 window.
// The native side only does what a web page cannot do inside this window: save a file the app made (backup),
// and open a link in the normal browser. Everything else is the web app itself.
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use base64::{engine::general_purpose::STANDARD, Engine};
use tauri::{Manager, WebviewUrl, WebviewWindowBuilder};

async fn blocking<T: Send + 'static>(f: impl FnOnce() -> T + Send + 'static) -> T {
    tauri::async_runtime::spawn_blocking(f).await.unwrap()
}

// Save a file the app made (the backup): asks where, returns the folder, or "" when cancelled.
#[tauri::command]
async fn save_file(name: String, b64: String) -> Result<String, String> {
    blocking(move || {
        let safe: String = name.chars().map(|c| if "\\/:*?\"<>|".contains(c) { '_' } else { c }).collect();
        let ext = safe.rsplit('.').next().unwrap_or("").to_string();
        let mut d = rfd::FileDialog::new().set_file_name(&safe);
        if !ext.is_empty() && ext != safe { d = d.add_filter(&ext.to_uppercase(), &[ext.as_str()]); }
        let Some(p) = d.save_file() else { return Ok(String::new()) };
        let bytes = STANDARD.decode(b64).map_err(|e| e.to_string())?;
        std::fs::write(&p, bytes).map_err(|e| e.to_string())?;
        Ok(p.parent().map(|x| x.to_string_lossy().into_owned()).unwrap_or_default())
    })
    .await
}

// Open a link (Sunnah.com, QuranEnc, a dictionary...) in the default browser. Only web, mail and phone links.
#[tauri::command]
async fn open_url(url: String) -> Result<(), String> {
    let u = url.to_ascii_lowercase();
    if !(u.starts_with("https://") || u.starts_with("http://") || u.starts_with("mailto:") || u.starts_with("tel:")) {
        return Err("only web, mail and phone links can be opened".into());
    }
    blocking(move || opener::open(&url).map_err(|e| e.to_string())).await
}

fn main() {
    tauri::Builder::default()
        // opening the app again brings the open window to the front instead of starting a second copy
        .plugin(tauri_plugin_single_instance::init(|app, _args, _cwd| {
            if let Some(w) = app.get_webview_window("main") {
                let _ = w.unminimize();
                let _ = w.show();
                let _ = w.set_focus();
            }
        }))
        .setup(|app| {
            let b = WebviewWindowBuilder::new(app, "main", WebviewUrl::App("index.html".into()))
                .title("My Personal Qur'an")
                .inner_size(1100.0, 860.0)
                .min_inner_size(380.0, 500.0)
                .center()
                .resizable(true)
                .disable_drag_drop_handler()
                .initialization_script(include_str!("shim.js"));
            // Only for the automatic check in CI (tests the installed app): when the environment variable MPQ_DEBUG_PORT
            // is set to a number, WebView2 listens for the test driver on that local port. Normal use never sets it.
            #[cfg(windows)]
            let b = match std::env::var("MPQ_DEBUG_PORT") {
                Ok(p) if !p.is_empty() && p.len() <= 5 && p.chars().all(|c| c.is_ascii_digit()) => b.additional_browser_args(&format!(
                    "--disable-features=msWebOOUI,msPdfOOUI,msSmartScreenProtection --remote-debugging-port={} --remote-allow-origins=*", p)),
                _ => b,
            };
            b.build()?;
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![save_file, open_url])
        .build(tauri::generate_context!())
        .expect("error while starting My Personal Qur'an")
        // when the window is closed, end the whole app at once
        .run(|app, event| match event {
            tauri::RunEvent::WindowEvent { event: tauri::WindowEvent::CloseRequested { .. }, .. } => { app.exit(0); }
            tauri::RunEvent::Exit => { std::process::exit(0); }
            _ => {}
        });
}
