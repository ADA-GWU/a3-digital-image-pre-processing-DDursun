import os
import requests
from io import BytesIO
import pydicom
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.gridspec as gridspec
from utils import apply_sharpening

# ownloading DICOM
file_id = '1X1o46ywbD_mcwVSGLdyNYYMCINiqxguK'
url = f'https://drive.google.com/uc?id={file_id}&export=download'
print("Downloading the DICOM...")
response = requests.get(url)
if response.status_code != 200:
    print("Download failed:", response.status_code)
    exit()
ds = pydicom.dcmread(BytesIO(response.content))

# Print metadata
print("=== DICOM Metadata (excluding Pixel Data) ===")
for elem in ds:
    if elem.tag != (0x7fe0, 0x0010):
        print(f"{elem.tag} {elem.description()} = {elem.value}")

# Load frames
if hasattr(ds, 'NumberOfFrames'):
    num_frames = int(ds.NumberOfFrames)
    frames = ds.pixel_array
else:
    num_frames = 1
    frames = [ds.pixel_array]

# Metadata block
def get_metadata_text(frame_num):
    return "\n".join([
        f"Modality:         {ds.get('Modality', 'N/A')}",
        f"Patient's Name:   {ds.get('PatientName', 'N/A')}",
        f"Patient ID:       {ds.get('PatientID', 'N/A')}",
        f"Study Date:       {ds.get('StudyDate', 'N/A')}",
        f"Frame Time:       {ds.get('FrameTime', 'N/A')}",
        f"Number of Frames: {num_frames}",
        f"Rows:             {ds.get('Rows', 'N/A')}",
        f"Columns:          {ds.get('Columns', 'N/A')}",
        f"Current Frame:    {frame_num}"
    ])

# Layout
fig = plt.figure(figsize=(16, 9))
gs = gridspec.GridSpec(2, 2, height_ratios=[8, 1], width_ratios=[5, 2])
gs.update(wspace=0.05, hspace=0.05)

ax_img = fig.add_subplot(gs[0, 0])
ax_img.set_position([0.05, 0.22, 0.62, 0.73])
img_display = ax_img.imshow(frames[0], cmap='gray', aspect='equal')
ax_img.set_title(f'MRI Image Frame 1 / {num_frames}', fontsize=14)
ax_img.axis('off')

# Right Panel
gs_right = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs[0, 1], height_ratios=[4, 1, 1], hspace=0.25)
ax_meta   = fig.add_subplot(gs_right[0])
ax_toggle = fig.add_subplot(gs_right[1])
ax_button = fig.add_subplot(gs_right[2])
slider_ax = fig.add_subplot(gs[1, :])

# Metadata
meta_text = ax_meta.text(0.02, 0.98, get_metadata_text(1),
                         transform=ax_meta.transAxes,
                         fontsize=12,
                         va='top',
                         ha='left',
                         family='monospace')
ax_meta.axis('off')

# Sharpen toggle button
sharpen_enabled = [False]
toggle_button = Button(ax_toggle, 'Sharpen: OFF', color='0.9', hovercolor='0.95')
toggle_button.label.set_fontsize(10)

def toggle_sharpen(event):
    sharpen_enabled[0] = not sharpen_enabled[0]
    toggle_button.label.set_text("Sharpen: ON" if sharpen_enabled[0] else "Sharpen: OFF")
    fig.canvas.draw_idle()

toggle_button.on_clicked(toggle_sharpen)

# Save button
save_button = Button(ax_button, 'Save as PNG', color='0.9', hovercolor='0.95')
save_button.label.set_fontsize(10)

status_text = ax_img.text(0.5, 0.05, "", transform=ax_img.transAxes,
                          fontsize=12, color='green', ha='center')

def clear_status():
    status_text.set_text("")
    fig.canvas.draw_idle()

def save_png(event):
    frame_num = int(frame_slider.val)
    img = frames[frame_num - 1]
    if sharpen_enabled[0]:
        img = apply_sharpening(img)
    os.makedirs('outputs/dicom', exist_ok=True)
    filename = f'outputs/dicom/frame_{frame_num}.png'
    plt.imsave(filename, img, cmap='gray')
    status_text.set_text(f"Frame {frame_num} saved successfully!")
    fig.canvas.draw_idle()
    timer = fig.canvas.new_timer(interval=2000)
    timer.add_callback(clear_status)
    timer.start()

save_button.on_clicked(save_png)

# Slider
frame_slider = Slider(slider_ax, 'Frame', 1, num_frames, valinit=1, valstep=1)

def update(val):
    frame_num = int(frame_slider.val)
    img_display.set_data(frames[frame_num - 1])
    ax_img.set_title(f'MRI Image Frame {frame_num} / {num_frames}', fontsize=14)
    meta_text.set_text(get_metadata_text(frame_num))
    fig.canvas.draw_idle()

frame_slider.on_changed(update)

plt.show()
