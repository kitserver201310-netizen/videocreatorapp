import streamlit as st
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# ---------------- Cấu hình trang ----------------
st.set_page_config(page_title="Video Creator App", page_icon="🎬", layout="centered")

st.title("🎬 Video Creator App")
st.divider()

# ---------------- Menu chức năng ----------------
chuc_nang = st.selectbox("Chọn chức năng bạn cần:", 
    ["🔊 Văn bản → Giọng nói", 
     "🖼️ Tạo ảnh nền cho video",
     "✍️ Tạo nội dung/script",
     "🎬 Tạo Video từ Ảnh + Âm thanh"])

st.divider()

# ---------------- Chức năng 1: Text to Speech ----------------
if chuc_nang == "🔊 Văn bản → Giọng nói":
    st.subheader("🔊 Chuyển Văn bản thành Giọng nói")
    
    van_ban = st.text_area("Nhập nội dung cần đọc:", 
        placeholder="Ví dụ: Chào mừng bạn đến với Video Creator App!", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        ngon_ngu = st.selectbox("Chọn ngôn ngữ:", ["vi - Tiếng Việt", "en - English"])
        ma_ngon_ngu = "vi" if ngon_ngu.startswith("vi") else "en"
    with col2:
        toc_do = st.radio("Tốc độ nói:", ["Chậm", "Bình thường"])
        cham = True if toc_do == "Chậm" else False
    
    tao = st.button("✨ Tạo giọng nói", type="primary", use_container_width=True)
    
    if tao and van_ban:
        with st.spinner("Đang tạo file âm thanh..."):
            tts = gTTS(text=van_ban, lang=ma_ngon_ngu, slow=cham)
            tep = io.BytesIO()
            tts.write_to_fp(tep)
            tep.seek(0)
            
            st.audio(tep, format="audio/mp3")
            st.success("✅ Tạo thành công! Nhấn nút ▶ để nghe hoặc ⬇ để tải về")
            
            st.download_button(label="⬇ Tải file MP3", data=tep, file_name="gioi_thieu.mp3", mime="audio/mpeg")

# ---------------- Chức năng 2: Tạo ảnh nền ----------------
elif chuc_nang == "🖼️ Tạo ảnh nền cho video":
    st.subheader("🖼️ Tạo ảnh nền đơn giản")
    
    mau_nen = st.color_picker("Màu nền", "#2E86AB")
    chu_nen = st.color_picker("Màu chữ", "#FFFFFF")
    kich_thuoc = st.selectbox("Kích thước ảnh:", ["1280x720 (HD)", "1080x1920 (Dọc điện thoại)"])
    
    rong, cao = (1280, 720) if kich_thuoc.startswith("1280") else (1080, 1920)
    
    chu_tren_anh = st.text_area("Chữ hiển thị trên ảnh:", 
        value="Video Creator\nApp", height=100)
    
    tao_anh = st.button("🎨 Tạo ảnh", type="primary", use_container_width=True)
    
    if tao_anh:
        with st.spinner("Đang tạo ảnh..."):
            anh = Image.new("RGB", (rong, cao), mau_nen)
            ve = ImageDraw.Draw(anh)
            
            try:
                font = ImageFont.truetype("arial.ttf", int(rong/12))
            except:
                font = ImageFont.load_default()
            
            vi_tri = (rong//2, cao//2)
            ve.text(vi_tri, chu_tren_anh, fill=chu_nen, font=font, anchor="mm", align="center")
            
            st.image(anh, caption="Ảnh nền của bạn", use_column_width=True)
            
            tep_anh = io.BytesIO()
            anh.save(tep_anh, format="PNG")
            tep_anh.seek(0)
            st.download_button(label="⬇ Tải ảnh PNG", data=tep_anh, file_name="anh_nen.png", mime="image/png")

# ---------------- Chức năng 3: Tạo script ----------------
elif chuc_nang == "✍️ Tạo nội dung/script":
    st.subheader("✍️ Soạn thảo nội dung video")
    
    chu_de = st.text_input("Tiêu đề video:", placeholder="Ví dụ: 5 Lý do nên dùng sản phẩm X")
    kieu_nd = st.selectbox("Loại nội dung:", ["Giới thiệu sản phẩm", "Review/Đánh giá", "Hướng dẫn", "Câu chuyện ngắn"])
    
    mau = {
        "Giới thiệu sản phẩm": """📌 {chu_de}

🔹 Ưu điểm 1: ...
🔹 Ưu điểm 2: ...
🔹 Ưu điểm 3: ...

👉 Liên hệ/Đặt hàng tại: ...
#Review #GioiThieu #SanPham""",
        "Review/Đánh giá": """⭐ Đánh giá: {chu_de}

✅ Điểm tốt:
- ...
- ...

⚠️ Cần cải thiện:
- ...

👉 Tổng kết: Đây là sản phẩm đáng tiền, nên thử một lần!
#Review #DanhGia #KinhNghiem""",
        "Hướng dẫn": """📖 Hướng dẫn: {chu_de}

Bước 1: ...
Bước 2: ...
Bước 3: ...

💡 Lưu ý quan trọng: ...
#HuongDan #CachLam #MeoNhanh""",
        "Câu chuyện ngắn": """📖 {chu_de}

[Mở đầu]
...

[Thân bài]
...

[Kết thúc]
...

#CauChuyen #DongLuc #CungDoc"""
    }
    
    if kieu_nd in mau:
        st.markdown("### 📝 Mẫu nội dung gợi ý:")
        nd_mau = mau[kieu_nd].replace("{chu_de}", chu_de if chu_de else "Tiêu đề của bạn")
        noi_dung = st.text_area("Nội dung script của bạn:", value=nd_mau, height=250)
        
        st.divider()
        st.code(noi_dung, language="markdown")
        st.success("✅ Bạn có thể copy nội dung trên để dùng cho video của mình!")

# ---------------- Chức năng 4: Tạo Video ----------------
elif chuc_nang == "🎬 Tạo Video từ Ảnh + Âm thanh":
    st.subheader("🎬 Tạo Video Ngắn")
    st.info("📌 Tải lên ảnh nền + file âm thanh → ứng dụng sẽ ghép thành video MP4")
    
    anh_nen = st.file_uploader("🖼️ Tải ảnh nền lên", type=["png", "jpg", "jpeg"])
    am_thanh = st.file_uploader("🔊 Tải file âm thanh lên", type=["mp3", "wav"])
    
    kich_thuoc = st.selectbox("Kích thước video:", ["1080x1920 (Dọc 9:16)", "1280x720 (Ngang 16:9)"])
    rong, cao = (1080, 1920) if kich_thuoc.startswith("1080") else (1280, 720)
    
    tao_video = st.button("✨ Tạo Video MP4", type="primary", use_container_width=True)
    
    if tao_video and anh_nen and am_thanh:
        with st.spinner("Đang tạo video... Vui lòng chờ 10-30 giây ⏳"):
            try:
                from moviepy.editor import ImageClip, AudioFileClip
                import tempfile, os
                
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                    f.write(anh_nen.read())
                    anh_path = f.name
                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                    f.write(am_thanh.read())
                    am_path = f.name
                
                clip_anh = ImageClip(anh_path).resize(width=rong, height=cao)
                clip_am = AudioFileClip(am_path)
                clip_video = clip_anh.set_duration(clip_am.duration)
                clip_video = clip_video.set_audio(clip_am)
                
                output_path = "video_ngat.mp4"
                clip_video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
                
                with open(output_path, "rb") as f:
                    video_bytes = f.read()
                
                st.success("✅ Tạo video thành công!")
                st.video(video_bytes, format="video/mp4")
                st.download_button("⬇ Tải file MP4", data=video_bytes, file_name="video_tao_ngat.mp4", mime="video/mp4")
                
                os.unlink(anh_path)
                os.unlink(am_path)
                os.unlink(output_path)
                
            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")
                st.info("💡 Nếu là lần đầu, hãy kiên nhẫn chờ 2-3 phút và thử lại nhé")
    elif tao_video:
        st.warning("⚠️ Vui lòng tải lên cả ảnh nền và file âm thanh trước!")

st.divider()
st.caption("💡 Mẹo: Sau khi tạo xong, hãy tải file về và ghép bằng công cụ chỉnh sửa video như CapCut nhé")
