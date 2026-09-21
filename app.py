import os
import base64
import streamlit as st
import streamlit.components.v1 as components

# 1. Streamlit 페이지 설정
st.set_page_config(
    page_title="Axport - Global Semiconductor Trade Intelligence",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 여백 완전 제거
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        border: none !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Base64 이미지 변환 헬퍼 (로컬 및 Streamlit Cloud 겸용)
def get_image_base64(filename, absolute_path=""):
    candidates = [
        absolute_path,
        filename,
        os.path.join(os.getcwd(), filename),
        os.path.join(os.path.dirname(__file__), filename) if '__file__' in globals() else "",
        os.path.join(r"C:\Users\user\Desktop\axport_demo_gemini", filename)
    ]
    for p in candidates:
        if p and os.path.exists(p) and os.path.isfile(p):
            try:
                with open(p, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode()
                    ext = os.path.splitext(p)[1].lower().replace('.', '')
                    mime = 'image/svg+xml' if ext == 'svg' else ('image/jpeg' if ext in ['jpg', 'jpeg'] else 'image/png')
                    return f"data:{mime};base64,{encoded}"
            except Exception:
                pass
    return ""

logo_b64 = get_image_base64("Axport_logo_png.png", r"C:\Users\user\Desktop\axport_demo_gemini\Axport_logo_png.png")
chatbot_b64 = get_image_base64("Axport_AI.png", r"C:\Users\user\Desktop\axport_demo_gemini\Axport_AI.png")

# 4. 전체 웹 애플리케이션 소스
raw_html = f"""
<!DOCTYPE html>
<html lang="ko" class="dark scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Axport - Semiconductor Trade Intelligence</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        brand: {{
                            50: '#eff6ff',
                            500: '#3b82f6',
                            600: '#2563eb',
                            700: '#1d4ed8',
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <!-- Three.js (r128) -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Inter:wght@400;500;600;700;800&display=swap');
        * {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }}
        
        .logo-font {{ font-family: 'Montserrat', sans-serif; font-weight: 900; }}

        /* 다크모드 로고 발광 필터 */
        .dark .logo-adaptive {{
            filter: brightness(0) invert(1) drop-shadow(0 0 6px rgba(56, 189, 248, 0.7));
        }}
        .logo-adaptive {{ transition: filter 0.3s ease; }}

        .mac-glass {{
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.5);
            box-shadow: 0 20px 45px -12px rgba(0, 0, 0, 0.35);
        }}
        .dark .mac-glass {{
            background: rgba(15, 23, 42, 0.88);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #f8fafc;
        }}
        .mac-desktop-bg {{
            background: radial-gradient(circle at 50% 20%, #1e3a8a 0%, #0f172a 60%, #020617 100%);
        }}

        /* 윈도우 크기 조절(Resizable) */
        .mac-window {{
            position: absolute;
            resize: both;
            overflow: auto;
            min-width: 280px;
            min-height: 180px;
            max-width: 90vw;
            max-height: 85vh;
        }}
        .window-drag-header {{ cursor: grab; user-select: none; }}
        .window-drag-header:active {{ cursor: grabbing; }}

        .kpi-gradient-blue {{ background: linear-gradient(135deg, #2563eb, #1d4ed8); }}
        .kpi-gradient-green {{ background: linear-gradient(135deg, #10b981, #059669); }}
        .kpi-gradient-purple {{ background: linear-gradient(135deg, #8b5cf6, #7c3aed); }}
        .kpi-gradient-amber {{ background: linear-gradient(135deg, #f59e0b, #d97706); }}

        .chatbot-container {{ box-shadow: 0 24px 48px -12px rgba(15, 23, 42, 0.45); }}
        .chat-bubble-ai {{ background: #F1F5F9; color: #0F172A; border-radius: 16px 16px 16px 4px; }}
        .dark .chat-bubble-ai {{ background: #1E293B; color: #F8FAFC; }}
        .chat-bubble-user {{ background: #0284C7; color: #FFFFFF; border-radius: 16px 16px 4px 16px; }}

        ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        ::-webkit-scrollbar-thumb {{ background: #64748b; border-radius: 4px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
    </style>
</head>
<body class="bg-white dark:bg-[#030712] text-slate-800 dark:text-slate-100 antialiased overflow-x-hidden min-h-screen transition-colors duration-300">

    <!-- 상단 글로벌 네비게이션 헤더 -->
    <header class="fixed top-0 left-0 right-0 z-50 bg-white/85 dark:bg-[#030712]/85 backdrop-blur-lg border-b border-slate-200 dark:border-slate-800/80 transition-all duration-300">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center gap-6">
                <!-- Axport 로고 -->
                <div class="cursor-pointer flex items-center select-none" onclick="switchView('landing')">
                    <img id="header-logo-img" src="{logo_b64}" alt="AXPORT" class="h-10 object-contain logo-adaptive" onerror="this.style.display='none'; document.getElementById('header-logo-fallback').style.display='block';" />
                    <div id="header-logo-fallback" class="hidden">
                        <span class="text-2xl font-black tracking-widest text-[#0E2344] dark:text-white">AXPORT</span>
                    </div>
                </div>

                <!-- 네비게이션 메뉴 (영문) -->
                <nav class="hidden md:flex items-center gap-1 bg-slate-100 dark:bg-slate-900/90 p-1 rounded-xl border border-slate-200 dark:border-slate-800">
                    <button onclick="switchView('landing')" id="nav-landing" class="px-4 py-1.5 rounded-lg text-sm font-semibold transition-all bg-blue-600 text-white shadow-sm">Home</button>
                    <button onclick="switchView('dashboard')" id="nav-dashboard" class="px-4 py-1.5 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-blue-600 dark:hover:text-white transition-all">Main Dashboard</button>
                    <button onclick="switchView('custom-mac')" id="nav-custom-mac" class="px-4 py-1.5 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-blue-600 dark:hover:text-white flex items-center gap-1.5 transition-all">
                        <i data-lucide="layout-grid" class="w-4 h-4"></i> Custom View
                    </button>
                </nav>
            </div>

            <!-- 우측 액션 버튼들 -->
            <div class="flex items-center gap-2 sm:gap-3">
                <button onclick="openContactModal()" class="flex items-center gap-1 text-xs font-semibold text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-cyan-400 px-2.5 py-1.5 rounded-lg border border-slate-300 dark:border-slate-700 transition-all">
                    <i data-lucide="mail" class="w-3.5 h-3.5"></i> Contact Us
                </button>

                <!-- 4개 국어 다국어 선택 -->
                <div class="relative">
                    <select id="lang-selector" onchange="changeLanguage(this.value)" class="bg-slate-100 dark:bg-slate-900 text-xs font-bold text-slate-700 dark:text-slate-300 rounded-lg px-2.5 py-1.5 border border-slate-300 dark:border-slate-700 focus:outline-none cursor-pointer">
                        <option value="ko">🇰🇷 한국어</option>
                        <option value="en">🇺🇸 English</option>
                        <option value="ja">🇯🇵 日本語</option>
                        <option value="zh">🇨🇳 中文</option>
                    </select>
                </div>

                <!-- 다크모드 토글 스위치 -->
                <button onclick="toggleDarkMode()" id="theme-toggle-btn" class="p-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-amber-400 border border-slate-300 dark:border-slate-700 hover:scale-105 transition-all">
                    <i id="theme-icon" data-lucide="sun" class="w-4 h-4"></i>
                </button>

                <button onclick="toggleChatbot()" class="hidden sm:flex items-center gap-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-3 py-1.5 rounded-lg shadow-sm transition-all">
                    <i data-lucide="bot" class="w-3.5 h-3.5"></i> Axport AI
                </button>
            </div>
        </div>
    </header>

    <!-- ================= VIEW 1: Home (HUD 디지털 홀로그램 3D 지구본) ================= -->
    <section id="view-landing" class="relative block w-full bg-white dark:bg-[#030712] transition-colors">
        <!-- 3D HUD 홀로그램 지구본 캔버스 -->
        <div id="canvas-sticky-wrap" class="fixed inset-0 z-0 pointer-events-none w-full h-full">
            <div id="globe-container" class="w-full h-full"></div>
        </div>

        <!-- 1단계: 진입 히어로 -->
        <div class="relative z-10 min-h-screen flex flex-col items-center justify-center text-center px-4 pt-16">
            <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-600 dark:text-cyan-300 text-xs font-semibold backdrop-blur-md mb-6 animate-pulse">
                <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
                <span id="txt-badge">HUD Futuristic Big Data Trade Intelligence</span>
            </div>
            <h1 class="text-4xl sm:text-7xl font-black tracking-tight text-slate-900 dark:text-white max-w-4xl leading-tight">
                <span id="txt-title1">반도체 수출 적합성의</span> <br>
                <span id="txt-title2" class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-cyan-400 to-indigo-600 dark:from-cyan-300 dark:via-blue-400 dark:to-indigo-300">새로운 기준, Axport</span>
            </h1>
            <p id="txt-subtitle" class="mt-6 text-slate-600 dark:text-slate-400 text-sm sm:text-lg max-w-xl leading-relaxed">
                실제 글로벌 무역망과 연결된 반도체 수출 통제 AI 진단 플랫폼
            </p>
            <div class="flex gap-4 mt-8 pointer-events-auto">
                <button onclick="switchView('dashboard')" class="bg-blue-600 hover:bg-blue-500 text-white font-bold px-6 py-3 rounded-xl shadow-lg shadow-blue-600/30 transition-all flex items-center gap-2 text-sm">
                    <i data-lucide="gauge" class="w-4 h-4"></i> <span id="txt-btn-dash">대시보드 시작하기</span>
                </button>
            </div>
        </div>

        <!-- 2단계: 회사 소개 -->
        <div class="relative z-10 min-h-screen flex items-center px-6 sm:px-16 py-24">
            <div class="max-w-xl bg-white/85 dark:bg-slate-950/85 backdrop-blur-xl p-8 sm:p-10 rounded-3xl border border-slate-200 dark:border-slate-800/80 shadow-2xl space-y-5">
                <div class="text-xs font-bold uppercase tracking-widest text-cyan-600 dark:text-cyan-400">About Axport</div>
                <h2 id="txt-about-h2" class="text-2xl sm:text-4xl font-extrabold text-slate-900 dark:text-white leading-tight">
                    복잡한 통제 규제를 <br>단 하나의 흐름으로
                </h2>
                <p id="txt-about-p" class="text-slate-600 dark:text-slate-300 text-sm leading-relaxed">
                    Axport는 기업의 원시 데이터(Raw CSV/ERP)를 실시간 스트리밍하여, 미 상무부 BIS 수출통제(ECCN 3A090)와 FTA 원산지 부가가치기준(RVC)을 완전 자동으로 판정합니다.
                </p>
                <div class="pt-2 flex items-center gap-6">
                    <div>
                        <div class="text-2xl font-black text-cyan-600 dark:text-cyan-400">99.8%</div>
                        <div class="text-xs text-slate-500 dark:text-slate-400">규제 판정 정확도</div>
                    </div>
                    <div class="w-px h-8 bg-slate-300 dark:bg-slate-800"></div>
                    <div>
                        <div class="text-2xl font-black text-blue-600 dark:text-blue-400">Zero-ETL</div>
                        <div class="text-xs text-slate-500 dark:text-slate-400">무가공 자동 정제</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 3단계: 핵심 강점 카드 -->
        <div class="relative z-10 max-w-7xl mx-auto px-6 py-24">
            <div class="text-center max-w-2xl mx-auto mb-16">
                <h3 class="text-xs font-bold uppercase tracking-wider text-cyan-600 dark:text-cyan-400 mb-2">Core Advantages</h3>
                <h4 class="text-3xl font-extrabold text-slate-900 dark:text-white">Axport 3단계 컴플라이언스 엔진</h4>
            </div>
            <div class="grid md:grid-cols-3 gap-6">
                <div class="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md p-8 rounded-2xl border border-slate-200 dark:border-slate-800/80 hover:border-cyan-500 transition-all group">
                    <div class="w-12 h-12 rounded-xl bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                        <i data-lucide="database" class="w-6 h-6"></i>
                    </div>
                    <h5 class="text-lg font-bold text-slate-900 dark:text-white mb-2">1. 원클릭 Zero-ETL</h5>
                    <p class="text-slate-600 dark:text-slate-400 text-xs leading-relaxed">기업마다 제각각인 ERP 인보이스 CSV를 올리기만 하면 통화 환산과 결측치를 알아서 정규화합니다.</p>
                </div>
                <div class="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md p-8 rounded-2xl border border-slate-200 dark:border-slate-800/80 hover:border-cyan-500 transition-all group">
                    <div class="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                        <i data-lucide="shield-check" class="w-6 h-6"></i>
                    </div>
                    <h5 class="text-lg font-bold text-slate-900 dark:text-white mb-2">2. 투명한 감점 원인 역추적</h5>
                    <p class="text-slate-600 dark:text-slate-400 text-xs leading-relaxed">ECCN 3A090 통제선 및 RVC 부가가치 미달 조항을 명확히 제시하며 담당자가 검수할 수 있습니다.</p>
                </div>
                <div class="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md p-8 rounded-2xl border border-slate-200 dark:border-slate-800/80 hover:border-cyan-500 transition-all group">
                    <div class="w-12 h-12 rounded-xl bg-purple-500/10 text-purple-600 dark:text-purple-400 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                        <i data-lucide="activity" class="w-6 h-6"></i>
                    </div>
                    <h5 class="text-lg font-bold text-slate-900 dark:text-white mb-2">3. 실시간 매크로 모니터링</h5>
                    <p class="text-slate-600 dark:text-slate-400 text-xs leading-relaxed">환율, DRAM 현물 가격, 대상국 세관 보류율을 실시간 동기화하여 물류 병목을 방지합니다.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- ================= VIEW 2: Main Dashboard ================= -->
    <section id="view-dashboard" class="hidden min-h-screen pt-20 px-4 sm:px-6 lg:px-8 pb-16 space-y-6 bg-slate-50 dark:bg-[#070D19] transition-colors">
        <div class="max-w-7xl mx-auto space-y-6">
            <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
                <div class="flex items-center gap-2 sm:gap-4 overflow-x-auto">
                    <button onclick="switchDashTab('tab-summary')" id="btntab-summary" class="dash-tab-btn px-4 py-2 text-sm font-bold border-b-2 border-blue-600 text-blue-600">📊 종합 요약</button>
                    <button onclick="switchDashTab('tab-upload')" id="btntab-upload" class="dash-tab-btn px-4 py-2 text-sm font-medium text-slate-500 hover:text-slate-900 dark:hover:text-white border-b-2 border-transparent">🔍 데이터 업로드 & 진단</button>
                    <button onclick="switchDashTab('tab-criteria')" id="btntab-criteria" class="dash-tab-btn px-4 py-2 text-sm font-medium text-slate-500 hover:text-slate-900 dark:hover:text-white border-b-2 border-transparent">📋 평가 기준 및 배점표</button>
                    <button onclick="switchDashTab('tab-risks')" id="btntab-risks" class="dash-tab-btn px-4 py-2 text-sm font-medium text-slate-500 hover:text-slate-900 dark:hover:text-white border-b-2 border-transparent">🛡️ 규제/통관 리스크</button>
                    <button onclick="switchDashTab('tab-macro')" id="btntab-macro" class="dash-tab-btn px-4 py-2 text-sm font-medium text-slate-500 hover:text-slate-900 dark:hover:text-white border-b-2 border-transparent">📈 시황 및 매크로</button>
                </div>
                <button onclick="switchView('custom-mac')" class="text-xs bg-slate-200 dark:bg-slate-800 hover:bg-slate-300 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-all">
                    <i data-lucide="layers" class="w-3.5 h-3.5"></i> Custom View 모드
                </button>
            </div>

            <!-- 종합 요약 -->
            <div id="content-tab-summary" class="space-y-6">
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div class="kpi-gradient-blue p-5 rounded-2xl text-white shadow-sm">
                        <div class="text-xs font-semibold uppercase tracking-wider opacity-85">총 수출액 (SEMICON)</div>
                        <div class="text-3xl font-extrabold mt-2">$12.8B</div>
                        <div class="text-xs mt-2 inline-flex items-center gap-1 bg-white/20 px-2.5 py-0.5 rounded-full font-medium">▲ 8.4% 전월 대비</div>
                    </div>
                    <div class="kpi-gradient-green p-5 rounded-2xl text-white shadow-sm">
                        <div class="text-xs font-semibold uppercase tracking-wider opacity-85">생산 가동률 (FAB)</div>
                        <div class="text-3xl font-extrabold mt-2">92.1%</div>
                        <div class="text-xs mt-2 inline-flex items-center gap-1 bg-white/20 px-2.5 py-0.5 rounded-full font-medium">▲ 2.3% 전월 대비</div>
                    </div>
                    <div class="kpi-gradient-purple p-5 rounded-2xl text-white shadow-sm">
                        <div class="text-xs font-semibold uppercase tracking-wider opacity-85">글로벌 수요 지수 (B/B)</div>
                        <div class="text-3xl font-extrabold mt-2">118.4</div>
                        <div class="text-xs mt-2 inline-flex items-center gap-1 bg-white/20 px-2.5 py-0.5 rounded-full font-medium">▼ 1.2% 전월 대비</div>
                    </div>
                    <div class="kpi-gradient-amber p-5 rounded-2xl text-white shadow-sm">
                        <div class="text-xs font-semibold uppercase tracking-wider opacity-85">신규 수주 잔고</div>
                        <div class="text-3xl font-extrabold mt-2">$3.4B</div>
                        <div class="text-xs mt-2 inline-flex items-center gap-1 bg-white/20 px-2.5 py-0.5 rounded-full font-medium">▲ 6.1% 전월 대비</div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="lg:col-span-2 bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-xs">
                        <div class="flex items-center justify-between mb-4">
                            <h4 class="font-bold text-slate-800 dark:text-slate-100 text-sm flex items-center gap-2">
                                <i data-lucide="trending-up" class="w-4 h-4 text-blue-600"></i> 월별 반도체 수출 추이 (YoY)
                            </h4>
                            <span class="text-xs text-slate-400">단위: Billion USD</span>
                        </div>
                        <div class="h-64 relative"><canvas id="chart-timeline"></canvas></div>
                    </div>
                    <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-xs">
                        <div class="flex items-center justify-between mb-4">
                            <h4 class="font-bold text-slate-800 dark:text-slate-100 text-sm flex items-center gap-2">
                                <i data-lucide="pie-chart" class="w-4 h-4 text-blue-600"></i> 주요국 수출 점유율
                            </h4>
                        </div>
                        <div class="h-64 relative flex items-center justify-center"><canvas id="chart-pie"></canvas></div>
                    </div>
                </div>

                <div class="bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-900 rounded-xl p-4 text-blue-900 dark:text-blue-200 text-xs leading-relaxed flex items-start gap-3">
                    <i data-lucide="info" class="w-5 h-5 text-blue-600 shrink-0 mt-0.5"></i>
                    <div>
                        <b>[시장 시사점 도출]</b> AI 가속기 및 HBM3e 중심의 고부가 패키징 수출 수요 확대로 대미 수출 점유율이 28%로 견고하게 유지되고 있습니다. 다만, 미 상무부 BIS의 첨단 컴퓨팅 칩(ECCN 3A090) 수출통제 개정으로 인해 동남아 우회 통관 시 최종 사용자(End-User) 검증 서약 절차를 보강할 필요가 있습니다.
                    </div>
                </div>
            </div>

            <!-- 데이터 업로드 탭 -->
            <div id="content-tab-upload" class="hidden space-y-6">
                <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-xs space-y-4">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                        <div>
                            <h3 class="text-lg font-bold text-slate-900 dark:text-white">반도체 원시 데이터(Raw File) 자동 전처리 및 평가</h3>
                            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">기업의 비정형 CSV 데이터를 업로드하면 결측치 보간, USD 환산 및 100점 만점 적합도를 즉시 산출합니다.</p>
                        </div>
                        <button onclick="downloadSampleCSV()" class="bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 font-semibold text-xs px-4 py-2.5 rounded-xl flex items-center gap-2 transition-all shrink-0 border border-slate-300 dark:border-slate-700">
                            <i data-lucide="download" class="w-4 h-4 text-blue-600"></i> 필수 항목 샘플(.csv) 다운로드
                        </button>
                    </div>

                    <div class="border-2 border-dashed border-slate-300 dark:border-slate-700 hover:border-cyan-500 rounded-2xl p-8 text-center transition-all cursor-pointer bg-slate-50/50 dark:bg-slate-800/30" onclick="document.getElementById('file-input').click()">
                        <input type="file" id="file-input" class="hidden" accept=".csv" onchange="handleFileUpload(event)">
                        <i data-lucide="upload-cloud" class="w-10 h-10 text-cyan-500 mx-auto mb-2"></i>
                        <p class="text-sm font-semibold text-slate-700 dark:text-slate-200">여기를 클릭하거나 CSV 파일을 드래그하여 업로드하세요</p>
                        <p class="text-xs text-slate-400 mt-1">지원 형식: .csv (HS_CODE, PRODUCT_NAME, PROCESS_NODE_NM, TARGET_COUNTRY 필수 포함)</p>
                    </div>
                </div>

                <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-xs space-y-4">
                    <div class="flex items-center justify-between">
                        <div>
                            <h4 class="font-bold text-slate-900 dark:text-white text-base">품목별 수출 적합성 진단 결과</h4>
                            <p class="text-xs text-slate-500 dark:text-slate-400">Zero-ETL 전처리 적용 완료 (USD 단위 정규화 및 결측치 보간)</p>
                        </div>
                        <div class="text-right">
                            <span class="text-xs text-slate-400">평균 적합도</span>
                            <div class="text-2xl font-black text-emerald-600 dark:text-emerald-400" id="total-score-badge">88.5점 (적합)</div>
                        </div>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-xs border-collapse">
                            <thead>
                                <tr class="bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 font-semibold border-b border-slate-200 dark:border-slate-700">
                                    <th class="p-3">HS CODE</th>
                                    <th class="p-3">품목명</th>
                                    <th class="p-3">공정 노드</th>
                                    <th class="p-3">수출 대상국</th>
                                    <th class="p-3">단가 (USD)</th>
                                    <th class="p-3">RVC 비율</th>
                                    <th class="p-3">판정 스코어</th>
                                    <th class="p-3">판정 근거 및 감점 요인</th>
                                </tr>
                            </thead>
                            <tbody id="diagnosis-tbody" class="divide-y divide-slate-100 dark:divide-slate-800 text-slate-700 dark:text-slate-200"></tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- 평가 기준표 탭 -->
            <div id="content-tab-criteria" class="hidden space-y-6">
                <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-xs space-y-6">
                    <div class="border-b border-slate-200 dark:border-slate-800 pb-4">
                        <h3 class="text-lg font-bold text-slate-900 dark:text-white">⚖️ Axport 반도체 수출 적합성 평가 기준 및 배점 체계</h3>
                        <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">국제 전략물자 통제 조약(바세나르 협정), 미 상무부 수출관리규정(EAR), 그리고 자유무역협정(FTA) 원산지 기준에 기반합니다.</p>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div class="p-4 rounded-xl border border-blue-200 dark:border-blue-900 bg-blue-50/50 dark:bg-blue-950/30">
                            <span class="text-xs font-bold text-blue-800 dark:text-blue-300">1. 기술 규제 적합도 (35점)</span>
                            <p class="text-[11px] text-slate-600 dark:text-slate-400 mt-2">• ECCN 3A090 통제선 미달 여부<br>• 웨이퍼 미세공정 (≤ 7nm 감점)<br>• TPP 연산능력 밀도 분석</p>
                        </div>
                        <div class="p-4 rounded-xl border border-emerald-200 dark:border-emerald-900 bg-emerald-50/50 dark:bg-emerald-950/30">
                            <span class="text-xs font-bold text-emerald-800 dark:text-emerald-300">2. 원산지 충족도 (30점)</span>
                            <p class="text-[11px] text-slate-600 dark:text-slate-400 mt-2">• 역내부가가치비율(RVC) 55% 이상<br>• 세번변경기준(CTSH) 충족성</p>
                        </div>
                        <div class="p-4 rounded-xl border border-amber-200 dark:border-amber-900 bg-amber-50/50 dark:bg-amber-950/30">
                            <span class="text-xs font-bold text-amber-800 dark:text-amber-300">3. 세관 통관 리스크 (20점)</span>
                            <p class="text-[11px] text-slate-600 dark:text-slate-400 mt-2">• 대상국 세관 평균 보류율<br>• 최종 사용자(End-User) 검증</p>
                        </div>
                        <div class="p-4 rounded-xl border border-purple-200 dark:border-purple-900 bg-purple-50/50 dark:bg-purple-950/30">
                            <span class="text-xs font-bold text-purple-800 dark:text-purple-300">4. 시장 가격 경쟁력 (15점)</span>
                            <p class="text-[11px] text-slate-600 dark:text-slate-400 mt-2">• 글로벌 DRAM/NAND 현물가 연동<br>• 외환 변동성 민감도 분석</p>
                        </div>
                    </div>

                    <table class="w-full text-xs text-left border-collapse border border-slate-200 dark:border-slate-700">
                        <thead class="bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-semibold">
                            <tr>
                                <th class="p-2.5 border border-slate-200 dark:border-slate-700">평가 항목</th>
                                <th class="p-2.5 border border-slate-200 dark:border-slate-700">정상 기준 (합격)</th>
                                <th class="p-2.5 border border-slate-200 dark:border-slate-700">감점 및 보완 조건</th>
                                <th class="p-2.5 border border-slate-200 dark:border-slate-700">적용 배점</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-200 dark:divide-slate-700 text-slate-600 dark:text-slate-300">
                            <tr>
                                <td class="p-2.5 border border-slate-200 dark:border-slate-700 font-semibold">전략물자 통제 (ECCN)</td>
                                <td class="p-2.5 border border-slate-200 dark:border-slate-700 text-emerald-600">EAR99 또는 범용 비통제 품목</td>
                                <td class="p-2.5 border border-slate-200 dark:border-slate-700 text-red-500">3A090 첨단 칩 또는 7nm 이하 미세공정 (-15점)</td>
                                <td class="p-2.5 border border-slate-200 dark:border-slate-700">35점 만점</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 border border-slate-200 dark:border-slate-700 font-semibold">원산지 부가가치 (RVC)</td>
                                <td class="p-2.5 border border-slate-200 dark:border-slate-700 text-emerald-600">RVC 55.0% 이상 확보</td>
                                <td class="p-2.5 border border-slate-200 dark:border-slate-700 text-red-500">RVC 55% 미만 시 FTA 혜택 제외 (-20점)</td>
                                <td class="p-2.5 border border-slate-200 dark:border-slate-700">30점 만점</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- 리스크 탭 -->
            <div id="content-tab-risks" class="hidden space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800">
                        <h4 class="font-bold text-slate-900 dark:text-white text-sm mb-4">미국 상무부 BIS 핵심 ECCN 통제 기준</h4>
                        <div class="space-y-3 text-xs">
                            <div class="p-3 bg-red-50 dark:bg-red-950/40 border-l-4 border-red-500 rounded-r-lg text-red-900 dark:text-red-200">
                                <b>ECCN 3A090.a (첨단 가속기 칩)</b>: TPP 4800 이상 고성능 가속기 칩은 사전 라이선스 의무화
                            </div>
                            <div class="p-3 bg-amber-50 dark:bg-amber-950/40 border-l-4 border-amber-500 rounded-r-lg text-amber-900 dark:text-amber-200">
                                <b>ECCN 3A090.b (성능 밀도 칩)</b>: 연산밀도 기준 충족 칩 사전 통보(NAC) 대상
                            </div>
                            <div class="p-3 bg-emerald-50 dark:bg-emerald-950/40 border-l-4 border-emerald-500 rounded-r-lg text-emerald-900 dark:text-emerald-200">
                                <b>EAR99 (범용 반도체)</b>: 성숙 공정(28nm 이상) 부품으로 통관 리스크 없음
                            </div>
                        </div>
                    </div>
                    <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800">
                        <h4 class="font-bold text-slate-900 dark:text-white text-sm mb-4">주요 수출 대상국별 세관 정밀 검사율</h4>
                        <div class="space-y-4 text-xs">
                            <div>
                                <div class="flex justify-between font-semibold mb-1"><span>미국 (CBP)</span><span>2.8% (양호)</span></div>
                                <div class="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden"><div class="bg-blue-600 h-full w-[28%]"></div></div>
                            </div>
                            <div>
                                <div class="flex justify-between font-semibold mb-1"><span>대만 (신주 FAB 경유)</span><span>1.4% (매우 양호)</span></div>
                                <div class="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden"><div class="bg-emerald-500 h-full w-[14%]"></div></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 시황 탭 -->
            <div id="content-tab-macro" class="hidden space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800">
                        <span class="text-xs text-slate-500">실시간 환율 (USD/KRW)</span>
                        <div class="text-2xl font-bold text-slate-900 dark:text-white mt-1">1,350.20 원</div>
                    </div>
                    <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800">
                        <span class="text-xs text-slate-500">DRAM DXI 현물 지수</span>
                        <div class="text-2xl font-bold text-slate-900 dark:text-white mt-1">28,450</div>
                    </div>
                    <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800">
                        <span class="text-xs text-slate-500">반도체 운임 지수 (SCFI)</span>
                        <div class="text-2xl font-bold text-slate-900 dark:text-white mt-1">1,940 pt</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- ================= VIEW 3: Custom View ================= -->
    <section id="view-custom-mac" class="hidden relative w-full h-[92vh] pt-16 mac-desktop-bg overflow-hidden">
        <div class="absolute top-20 left-1/2 -translate-x-1/2 z-50 flex items-center gap-2 bg-white/20 dark:bg-black/40 backdrop-blur-xl border border-white/30 px-4 py-2 rounded-2xl shadow-xl">
            <button onclick="toggleMacWindow('mac-win1')" id="btn-win1" class="px-3.5 py-1.5 rounded-xl text-xs font-semibold text-white bg-blue-600 shadow-md flex items-center gap-1.5">
                <i data-lucide="bar-chart-2" class="w-3.5 h-3.5"></i> KPI 창
            </button>
            <button onclick="toggleMacWindow('mac-win2')" id="btn-win2" class="px-3.5 py-1.5 rounded-xl text-xs font-semibold text-white bg-blue-600 shadow-md flex items-center gap-1.5">
                <i data-lucide="shield-check" class="w-3.5 h-3.5"></i> 적합도 진단 창
            </button>
            <button onclick="toggleMacWindow('mac-win3')" id="btn-win3" class="px-3.5 py-1.5 rounded-xl text-xs font-semibold text-white bg-blue-600 shadow-md flex items-center gap-1.5">
                <i data-lucide="alert-triangle" class="w-3.5 h-3.5"></i> 리스크 창
            </button>
            <button onclick="toggleMacWindow('mac-win4')" id="btn-win4" class="px-3.5 py-1.5 rounded-xl text-xs font-semibold text-white bg-blue-600 shadow-md flex items-center gap-1.5">
                <i data-lucide="trending-up" class="w-3.5 h-3.5"></i> 시황 창
            </button>
        </div>

        <div id="mac-win1" class="mac-window w-80 mac-glass rounded-2xl shadow-2xl" style="top: 120px; left: 40px; z-index: 20;">
            <div class="window-drag-header bg-slate-100/70 dark:bg-slate-800/70 border-b border-slate-200/50 px-3.5 py-2.5 flex items-center justify-between">
                <span class="text-xs font-semibold">SEMICON KPI 요약</span>
                <span class="text-[10px] text-slate-400">드래그/크기조절 가능</span>
            </div>
            <div class="p-4 space-y-3">
                <div class="p-3 rounded-xl bg-blue-50/80 dark:bg-blue-950/40 border border-blue-100 dark:border-blue-900">
                    <span class="text-[11px] font-bold text-blue-600 dark:text-cyan-400 uppercase">총 수출액</span>
                    <div class="text-2xl font-black text-blue-900 dark:text-white">$12.8B</div>
                    <span class="text-[11px] text-emerald-600 dark:text-emerald-400 font-semibold">▲ 8.4% 전월 대비</span>
                </div>
            </div>
        </div>

        <div id="mac-win2" class="mac-window w-96 mac-glass rounded-2xl shadow-2xl" style="top: 120px; left: 380px; z-index: 21;">
            <div class="window-drag-header bg-slate-100/70 dark:bg-slate-800/70 border-b border-slate-200/50 px-3.5 py-2.5 flex items-center justify-between">
                <span class="text-xs font-semibold">수출 적합성 진단 엔진</span>
                <span class="text-[10px] text-slate-400">드래그/크기조절 가능</span>
            </div>
            <div class="p-4 space-y-3 text-xs">
                <div class="flex items-center justify-between pb-2 border-b border-slate-200 dark:border-slate-700">
                    <span class="font-bold">진단 종합 결과</span>
                    <span class="px-2.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300 font-bold">88.5점 (합격)</span>
                </div>
                <div class="space-y-1 text-slate-600 dark:text-slate-300">
                    <div>• ECCN 3A090 검토: <b>해당 없음 (Pass)</b></div>
                    <div>• RVC 부가가치비율: <b>65.2% (충족)</b></div>
                </div>
            </div>
        </div>

        <div id="mac-win3" class="mac-window w-84 mac-glass rounded-2xl shadow-2xl" style="top: 320px; left: 100px; z-index: 22;">
            <div class="window-drag-header bg-slate-100/70 dark:bg-slate-800/70 border-b border-slate-200/50 px-3.5 py-2.5 flex items-center justify-between">
                <span class="text-xs font-semibold">통관 리스크 모니터</span>
            </div>
            <div class="p-4 text-xs">
                <div class="p-2.5 bg-amber-50 dark:bg-amber-950/40 rounded-xl border border-amber-200 dark:border-amber-900 text-amber-900 dark:text-amber-200">
                    <b>⚠️ 세관 점검 권고</b><br>
                    대만 신주 경유 건 End-User 서약서 첨부 요망
                </div>
            </div>
        </div>

        <div id="mac-win4" class="mac-window w-80 mac-glass rounded-2xl shadow-2xl" style="top: 300px; left: 520px; z-index: 23;">
            <div class="window-drag-header bg-slate-100/70 dark:bg-slate-800/70 border-b border-slate-200/50 px-3.5 py-2.5 flex items-center justify-between">
                <span class="text-xs font-semibold">FX & Spot Feed</span>
            </div>
            <div class="p-4 text-xs space-y-2">
                <div class="flex justify-between"><span>USD / KRW</span><b>1,350.2 원 (+3.2)</b></div>
                <div class="flex justify-between"><span>DRAM DXI</span><b>$4.25 (▲ 2.1%)</b></div>
            </div>
        </div>
    </section>

    <!-- ================= Contact Us 모달 ================= -->
    <div id="modal-contact" class="hidden fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
        <div class="bg-white dark:bg-slate-900 max-w-md w-full rounded-3xl p-6 shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
            <div class="flex justify-between items-center border-b border-slate-200 dark:border-slate-800 pb-3">
                <h3 class="font-bold text-slate-900 dark:text-white text-base flex items-center gap-2">
                    <i data-lucide="mail" class="w-4 h-4 text-cyan-500"></i> Contact Axport
                </h3>
                <button onclick="closeContactModal()" class="text-slate-400 hover:text-slate-600 dark:hover:text-white"><i data-lucide="x" class="w-5 h-5"></i></button>
            </div>
            <div class="space-y-3 text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                <div class="p-3 bg-cyan-50 dark:bg-cyan-950/40 rounded-xl border border-cyan-200 dark:border-cyan-800 text-cyan-900 dark:text-cyan-200 font-medium">
                    📌 <b>안내</b>: 공식 고객센터 및 무역 실무 전담팀 연락처는 <b>정식 릴리즈 버전에 맞춰 업데이트 예정</b>입니다.
                </div>
                <div>
                    <label class="block font-semibold mb-1">문의 및 제휴 이메일 남기기</label>
                    <input type="email" placeholder="name@company.com" class="w-full bg-slate-100 dark:bg-slate-800 border-none rounded-xl p-2.5 text-xs text-slate-800 dark:text-slate-100 focus:outline-none" />
                </div>
            </div>
            <div class="flex justify-end gap-2 pt-2">
                <button onclick="closeContactModal()" class="px-4 py-2 rounded-xl text-xs font-semibold text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800">닫기</button>
                <button onclick="alert('문의가 접수되었습니다. 업데이트 후 회신 드리겠습니다.'); closeContactModal();" class="bg-cyan-600 text-white font-bold text-xs px-4 py-2 rounded-xl shadow-md">접수하기</button>
            </div>
        </div>
    </div>

    <!-- ================= 플로팅 AI 챗봇 ================= -->
    <div id="chatbot-trigger" onclick="toggleChatbot()" class="fixed bottom-6 right-6 z-50 cursor-pointer group">
        <div class="relative w-14 h-14 rounded-full bg-gradient-to-tr from-cyan-600 to-blue-600 flex items-center justify-center text-white shadow-2xl hover:scale-105 transition-transform overflow-hidden border-2 border-white dark:border-slate-800">
            <img id="chat-fab-img" src="{chatbot_b64}" alt="AI" class="w-full h-full object-cover" onerror="this.style.display='none'; document.getElementById('chat-fab-fallback').style.display='flex';" />
            <div id="chat-fab-fallback" class="hidden w-full h-full items-center justify-center bg-gradient-to-tr from-cyan-600 to-blue-600">
                <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 8V4H8"></path>
                    <rect width="16" height="12" x="4" y="8" rx="2"></rect>
                    <path d="M2 14h2"></path>
                    <path d="M20 14h2"></path>
                    <path d="M15 13v2"></path>
                    <path d="M9 13v2"></path>
                </svg>
            </div>
            <span class="absolute top-0 right-0 w-3.5 h-3.5 rounded-full bg-emerald-400 border-2 border-white"></span>
        </div>
    </div>

    <div id="chatbot-window" class="hidden fixed bottom-24 right-6 z-50 w-96 max-w-[90vw] h-[520px] bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 chatbot-container flex flex-col overflow-hidden">
        <div class="bg-gradient-to-r from-cyan-600 to-blue-800 p-4 text-white flex items-center justify-between">
            <div class="flex items-center gap-2.5">
                <div class="w-8 h-8 rounded-full bg-white/20 p-0.5 overflow-hidden border border-white/40 flex items-center justify-center">
                    <img id="chat-header-img" src="{chatbot_b64}" alt="AI" class="w-full h-full object-cover rounded-full" onerror="this.style.display='none'; document.getElementById('chat-header-fallback').style.display='block';" />
                    <div id="chat-header-fallback" class="hidden text-white"><i data-lucide="bot" class="w-5 h-5"></i></div>
                </div>
                <div>
                    <h4 class="font-bold text-sm text-white">Axport AI 어시스턴트</h4>
                    <p class="text-[10px] text-cyan-200">반도체 수출통제 전담 AI</p>
                </div>
            </div>
            <button onclick="toggleChatbot()" class="text-white/80 hover:text-white p-1"><i data-lucide="x" class="w-5 h-5"></i></button>
        </div>

        <div class="p-2.5 bg-slate-50 dark:bg-slate-800 border-b border-slate-100 dark:border-slate-700 flex gap-1.5 overflow-x-auto text-[11px]">
            <button onclick="askPreset('ECCN 3A090 규제 기준이 뭐야?')" class="px-2.5 py-1 rounded-full bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 text-slate-700 dark:text-slate-200 whitespace-nowrap">3A090 통제선</button>
            <button onclick="askPreset('RVC 부가가치기준 계산법 알려줘')" class="px-2.5 py-1 rounded-full bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 text-slate-700 dark:text-slate-200 whitespace-nowrap">RVC 산출 공식</button>
            <button onclick="askPreset('HBM3e 대미 수출 시 주의점은?')" class="px-2.5 py-1 rounded-full bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 text-slate-700 dark:text-slate-200 whitespace-nowrap">HBM 대미 수출</button>
        </div>

        <div id="chat-messages" class="flex-1 p-4 overflow-y-auto space-y-3 text-xs text-slate-800 dark:text-slate-100">
            <div class="flex items-start gap-2">
                <div class="chat-bubble-ai p-3 max-w-[85%] leading-relaxed">
                    안녕하세요! <b>Axport 반도체 무역 규제 전담 AI</b>입니다.<br>ECCN 전략물자 통제, FTA 원산지 RVC 산출 등 궁금한 점을 질문하세요.
                </div>
            </div>
        </div>

        <div class="p-3 bg-white dark:bg-slate-900 border-t border-slate-100 dark:border-slate-800">
            <form id="chat-form" onsubmit="handleChatSubmit(event)" class="flex items-center gap-2">
                <input type="text" id="chat-input" placeholder="질문 입력..." class="flex-1 bg-slate-100 dark:bg-slate-800 border-none rounded-xl px-3.5 py-2.5 text-xs text-slate-800 dark:text-slate-100 focus:outline-none" />
                <button type="submit" class="bg-cyan-600 text-white p-2.5 rounded-xl"><i data-lucide="send" class="w-4 h-4"></i></button>
            </form>
        </div>
    </div>

    <!-- ================= JS: Storyblocks HUD 디지털 미래형 지구본 3D 엔진 ================= -->
    <script>
        lucide.createIcons();

        // 1. 테마 토글
        function toggleDarkMode() {{
            const html = document.documentElement;
            const isDark = html.classList.contains('dark');
            const icon = document.getElementById('theme-icon');
            if (isDark) {{
                html.classList.remove('dark');
                icon.setAttribute('data-lucide', 'moon');
                localStorage.setItem('axport-theme', 'light');
            }} else {{
                html.classList.add('dark');
                icon.setAttribute('data-lucide', 'sun');
                localStorage.setItem('axport-theme', 'dark');
            }}
            lucide.createIcons();
        }}

        // 2. 다국어
        const i18n = {{
            ko: {{ badge: "HUD Futuristic Big Data Trade Intelligence", title1: "반도체 수출 적합성의", title2: "새로운 기준, Axport", subtitle: "실제 글로벌 무역망과 연결된 반도체 수출 통제 AI 진단 플랫폼", btnDash: "대시보드 시작하기", aboutH2: "복잡한 통제 규제를 <br>단 하나의 흐름으로", aboutP: "Axport는 기업의 원시 데이터를 실시간 스트리밍하여, 미 상무부 BIS 수출통제와 FTA 부가가치기준을 완전 자동으로 판정합니다." }},
            en: {{ badge: "HUD Futuristic Big Data Trade Intelligence", title1: "A New Standard for", title2: "Semiconductor Export, Axport", subtitle: "AI-Powered Semiconductor Export Compliance Platform Connected to Global Trade Networks", btnDash: "Launch Dashboard", aboutH2: "Complex Trade Regulations <br>In a Single Seamless Flow", aboutP: "Axport automatically streams raw ERP data to audit US BIS ECCN controls and FTA Regional Value Content in real time." }},
            ja: {{ badge: "HUD Futuristic Big Data Trade Intelligence", title1: "半導体輸出適合性の", title2: "新たな基準、Axport", subtitle: "グローバル貿易ネットワークと直結した半導体輸出管理AIプラットフォーム", btnDash: "ダッシュボードを開始", aboutH2: "複雑な規制対応を <br>ひとつのスムーズな流れに", aboutP: "Axportは企業の生データを直接解析し、米BIS ECCN規制およびFTA原産地付加価値基準を自動診断します。" }},
            zh: {{ badge: "HUD Futuristic Big Data Trade Intelligence", title1: "半导体出口合规的", title2: "全新标准，Axport", subtitle: "深度连接全球贸易网络的半导体出口合规人工智能平台", btnDash: "进入数据看板", aboutH2: "化繁为简 <br>一体化智能合规流程", aboutP: "Axport实时解析企业ERP原始数据，全面自动核查美国BIS ECCN出口管制及FTA区域价值成分。" }}
        }};

        function changeLanguage(lang) {{
            const t = i18n[lang] || i18n.ko;
            document.getElementById('txt-badge').innerText = t.badge;
            document.getElementById('txt-title1').innerText = t.title1;
            document.getElementById('txt-title2').innerText = t.title2;
            document.getElementById('txt-subtitle').innerText = t.subtitle;
            document.getElementById('txt-btn-dash').innerText = t.btnDash;
            document.getElementById('txt-about-h2').innerHTML = t.aboutH2;
            document.getElementById('txt-about-p').innerText = t.aboutP;
        }}

        function openContactModal() {{ document.getElementById('modal-contact').classList.remove('hidden'); }}
        function closeContactModal() {{ document.getElementById('modal-contact').classList.add('hidden'); }}

        // 3. 뷰 전환
        function switchView(viewId) {{
            document.getElementById('view-landing').classList.add('hidden');
            document.getElementById('view-dashboard').classList.add('hidden');
            document.getElementById('view-custom-mac').classList.add('hidden');
            document.getElementById('canvas-sticky-wrap').classList.add('hidden');

            document.getElementById('nav-landing').className = "px-4 py-1.5 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-blue-600 dark:hover:text-white transition-all";
            document.getElementById('nav-dashboard').className = "px-4 py-1.5 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-blue-600 dark:hover:text-white transition-all";
            document.getElementById('nav-custom-mac').className = "px-4 py-1.5 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-blue-600 dark:hover:text-white flex items-center gap-1.5 transition-all";

            if(viewId === 'landing') {{
                document.getElementById('view-landing').classList.remove('hidden');
                document.getElementById('canvas-sticky-wrap').classList.remove('hidden');
                document.getElementById('nav-landing').className = "px-4 py-1.5 rounded-lg text-sm font-semibold transition-all bg-blue-600 text-white shadow-sm";
            }} else if(viewId === 'dashboard') {{
                document.getElementById('view-dashboard').classList.remove('hidden');
                document.getElementById('nav-dashboard').className = "px-4 py-1.5 rounded-lg text-sm font-semibold transition-all bg-blue-600 text-white shadow-sm";
                setTimeout(() => {{ initOrUpdateCharts(); }}, 50);
            }} else if(viewId === 'custom-mac') {{
                document.getElementById('view-custom-mac').classList.remove('hidden');
                document.getElementById('nav-custom-mac').className = "px-4 py-1.5 rounded-lg text-sm font-semibold transition-all bg-blue-600 text-white shadow-sm flex items-center gap-1.5";
            }}
        }}

        function switchDashTab(tabId) {{
            ['tab-summary', 'tab-upload', 'tab-criteria', 'tab-risks', 'tab-macro'].forEach(t => {{
                const content = document.getElementById('content-' + t);
                const btn = document.getElementById('btntab-' + t);
                if(content) content.classList.add('hidden');
                if(btn) btn.className = "dash-tab-btn px-4 py-2 text-sm font-medium text-slate-500 hover:text-slate-900 dark:hover:text-white border-b-2 border-transparent";
            }});
            const targetContent = document.getElementById('content-' + tabId);
            const targetBtn = document.getElementById('btntab-' + tabId);
            if(targetContent) targetContent.classList.remove('hidden');
            if(targetBtn) targetBtn.className = "dash-tab-btn px-4 py-2 text-sm font-bold border-b-2 border-blue-600 text-blue-600";
            if(tabId === 'tab-summary') {{ setTimeout(() => {{ initOrUpdateCharts(); }}, 50); }}
        }}

        // 4. [Storyblocks HUD 미래형 디지털 지구본 3D 엔진]
        let globeScene, globeCamera, globeRenderer, globeGroup, hudGroup;
        let hudRing1, hudRing2, hudRing3, hudTickRing, hudBrackets;
        let baseRadius = 55;
        let scrollYProgress = 0;

        function latLonToVec3(lat, lon, radius) {{
            const phi = (90 - lat) * (Math.PI / 180);
            const theta = (lon + 180) * (Math.PI / 180);
            return new THREE.Vector3(
                -(radius * Math.sin(phi) * Math.cos(theta)),
                radius * Math.cos(phi),
                radius * Math.sin(phi) * Math.sin(theta)
            );
        }}

        // 영상과 일치하는 실제 세계 대륙 도트/선 실루엣 텍스처
        function createHUDContinentTexture() {{
            const canvas = document.createElement('canvas');
            canvas.width = 2048;
            canvas.height = 1024;
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 대륙 경계선 및 내부 도트 매트릭스 필
            ctx.fillStyle = 'rgba(0, 240, 255, 0.45)';
            ctx.strokeStyle = '#38bdf8';
            ctx.lineWidth = 2.5;

            function drawLand(coords) {{
                ctx.beginPath();
                coords.forEach(([lon, lat], idx) => {{
                    const x = (lon + 180) * (canvas.width / 360);
                    const y = (90 - lat) * (canvas.height / 180);
                    if (idx === 0) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);
                }});
                ctx.closePath();
                ctx.fill();
                ctx.stroke();
            }}

            drawLand([[125, 42], [130, 42], [129, 35], [126, 34], [125, 38]]); // 한국
            drawLand([[130, 32], [136, 35], [141, 44], [143, 42], [139, 36], [131, 31]]); // 일본
            drawLand([
                [30, 70], [60, 72], [100, 75], [140, 72], [170, 65], [140, 50], [130, 43],
                [122, 30], [108, 20], [100, 10], [90, 22], [80, 10], [70, 25], [60, 25],
                [50, 30], [35, 32], [28, 41], [15, 55], [10, 60], [25, 68]
            ]);
            drawLand([
                [-168, 65], [-140, 70], [-90, 72], [-60, 60], [-65, 45], [-75, 35], [-80, 25],
                [-97, 26], [-105, 20], [-118, 32], [-124, 48], [-130, 55], [-160, 58]
            ]);
            drawLand([
                [-75, 10], [-50, -5], [-35, -5], [-40, -22], [-55, -38], [-68, -55], [-75, -45],
                [-72, -20], [-80, -2]
            ]);
            drawLand([
                [-10, 36], [0, 43], [5, 50], [2, 58], [15, 58], [25, 60], [30, 50], [20, 40], [0, 38]
            ]);
            drawLand([
                [-15, 30], [10, 37], [30, 32], [42, 12], [50, 10], [40, -10], [30, -32],
                [18, -34], [10, -5], [-10, 5], [-17, 15]
            ]);
            drawLand([
                [115, -22], [130, -12], [142, -10], [150, -24], [145, -38], [130, -32], [115, -34]
            ]);

            return new THREE.CanvasTexture(canvas);
        }}

        // HUD 눈금 텍스처 (영상에 나오는 인터페이스 눈금 링)
        function createTickRingTexture() {{
            const canvas = document.createElement('canvas');
            canvas.width = 1024;
            canvas.height = 128;
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.strokeStyle = '#00f0ff';
            ctx.lineWidth = 2;
            for(let x = 0; x < canvas.width; x += 16) {{
                const h = (x % 64 === 0) ? 90 : 45;
                ctx.beginPath();
                ctx.moveTo(x, 64 - h/2);
                ctx.lineTo(x, 64 + h/2);
                ctx.stroke();
            }}
            const tex = new THREE.CanvasTexture(canvas);
            tex.wrapS = THREE.RepeatWrapping;
            tex.repeat.set(4, 1);
            return tex;
        }}

        function init3DGlobe() {{
            const container = document.getElementById('globe-container');
            if(!container) return;

            globeScene = new THREE.Scene();
            globeCamera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
            globeCamera.position.set(0, 0, 165);

            globeRenderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            globeRenderer.setSize(window.innerWidth, window.innerHeight);
            globeRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            container.appendChild(globeRenderer.domElement);

            globeGroup = new THREE.Group();
            globeScene.add(globeGroup);

            // 1. 내부 딥 블루 코어 구체
            const coreGeo = new THREE.SphereGeometry(baseRadius - 0.6, 48, 48);
            const coreMat = new THREE.MeshBasicMaterial({{ color: 0x051329, transparent: true, opacity: 0.9 }});
            globeGroup.add(new THREE.Mesh(coreGeo, coreMat));

            // 2. 영상의 선명한 홀로그램 대륙 껍질
            const continentTex = createHUDContinentTexture();
            const globeGeo = new THREE.SphereGeometry(baseRadius, 64, 64);
            const globeMat = new THREE.MeshBasicMaterial({{
                map: continentTex,
                transparent: true,
                opacity: 0.95,
                blending: THREE.AdditiveBlending
            }});
            const continentMesh = new THREE.Mesh(globeGeo, globeMat);
            globeGroup.add(continentMesh);

            // 3. 정밀 위도/경도 경량 격자망
            const gridGeo = new THREE.SphereGeometry(baseRadius + 0.3, 36, 18);
            const gridMat = new THREE.MeshBasicMaterial({{
                color: 0x00f0ff,
                wireframe: true,
                transparent: true,
                opacity: 0.2
            }});
            globeGroup.add(new THREE.Mesh(gridGeo, gridMat));

            // 4. [영상 핵심 요소] HUD 인터페이스 다층 링 & 조준 시스템
            hudGroup = new THREE.Group();
            globeGroup.add(hudGroup);

            // A. 적도 눈금 링 (HUD Tick Ring)
            const tickGeo = new THREE.RingGeometry(baseRadius * 1.22, baseRadius * 1.28, 64);
            const tickMat = new THREE.MeshBasicMaterial({{
                map: createTickRingTexture(),
                side: THREE.DoubleSide,
                transparent: true,
                opacity: 0.8,
                blending: THREE.AdditiveBlending
            }});
            hudTickRing = new THREE.Mesh(tickGeo, tickMat);
            hudTickRing.rotation.x = Math.PI / 2;
            hudGroup.add(hudTickRing);

            // B. 기울어진 궤도 점선 링 1
            const ringGeo1 = new THREE.RingGeometry(baseRadius * 1.36, baseRadius * 1.38, 64);
            const ringMat1 = new THREE.MeshBasicMaterial({{
                color: 0x38bdf8,
                side: THREE.DoubleSide,
                transparent: true,
                opacity: 0.6,
                blending: THREE.AdditiveBlending
            }});
            hudRing1 = new THREE.Mesh(ringGeo1, ringMat1);
            hudRing1.rotation.x = Math.PI / 3;
            hudGroup.add(hudRing1);

            // C. 역방향 오비탈 링 2
            const ringGeo2 = new THREE.RingGeometry(baseRadius * 1.48, baseRadius * 1.50, 64);
            const ringMat2 = new THREE.MeshBasicMaterial({{
                color: 0x00f0ff,
                side: THREE.DoubleSide,
                transparent: true,
                opacity: 0.45,
                blending: THREE.AdditiveBlending
            }});
            hudRing2 = new THREE.Mesh(ringGeo2, ringMat2);
            hudRing2.rotation.x = -Math.PI / 4;
            hudGroup.add(hudRing2);

            // D. HUD 타깃 브래킷 (네 귀퉁이 조준선)
            hudBrackets = new THREE.Group();
            hudGroup.add(hudBrackets);
            const bracketMat = new THREE.LineBasicMaterial({{ color: 0x00f0ff, transparent: true, opacity: 0.7 }});
            const bR = baseRadius * 1.6;
            const bPts = [
                // Top-Left bracket
                [new THREE.Vector3(-bR, bR * 0.8, 0), new THREE.Vector3(-bR, bR, 0)],
                [new THREE.Vector3(-bR, bR, 0), new THREE.Vector3(-bR * 0.8, bR, 0)],
                // Top-Right bracket
                [new THREE.Vector3(bR * 0.8, bR, 0), new THREE.Vector3(bR, bR, 0)],
                [new THREE.Vector3(bR, bR, 0), new THREE.Vector3(bR, bR * 0.8, 0)],
                // Bottom-Left
                [new THREE.Vector3(-bR, -bR * 0.8, 0), new THREE.Vector3(-bR, -bR, 0)],
                [new THREE.Vector3(-bR, -bR, 0), new THREE.Vector3(-bR * 0.8, -bR, 0)],
                // Bottom-Right
                [new THREE.Vector3(bR * 0.8, -bR, 0), new THREE.Vector3(bR, -bR, 0)],
                [new THREE.Vector3(bR, -bR, 0), new THREE.Vector3(bR, -bR * 0.8, 0)],
            ];
            bPts.forEach(([p1, p2]) => {{
                const geo = new THREE.BufferGeometry().setFromPoints([p1, p2]);
                hudBrackets.add(new THREE.Line(geo, bracketMat));
            }});

            // 5. 빅데이터 무역 공급망 발광 노드 및 아크
            const hubs = [
                {{ lat: 37.56, lon: 126.97 }},  // 한국
                {{ lat: 37.77, lon: -122.41 }}, // 미국 실리콘밸리
                {{ lat: 24.78, lon: 120.99 }},  // 대만
                {{ lat: 21.02, lon: 105.83 }},  // 베트남
                {{ lat: 51.05, lon: 13.73 }}    // 유럽
            ];

            hubs.forEach(h => {{
                const pos = latLonToVec3(h.lat, h.lon, baseRadius + 0.5);
                const dot = new THREE.Mesh(
                    new THREE.SphereGeometry(1.6, 12, 12),
                    new THREE.MeshBasicMaterial({{ color: 0x67e8f9 }})
                );
                dot.position.copy(pos);
                globeGroup.add(dot);

                // 수직 데이터 기둥 (Big Data Pillar)
                const p2 = pos.clone().multiplyScalar(1.12);
                const colGeo = new THREE.BufferGeometry().setFromPoints([pos, p2]);
                const colMat = new THREE.LineBasicMaterial({{ color: 0x00f0ff, transparent: true, opacity: 0.8 }});
                globeGroup.add(new THREE.Line(colGeo, colMat));
            }});

            function addTradeArc(from, to) {{
                const p1 = latLonToVec3(from.lat, from.lon, baseRadius + 0.5);
                const p2 = latLonToVec3(to.lat, to.lon, baseRadius + 0.5);
                const mid = p1.clone().add(p2).multiplyScalar(0.5);
                const dist = p1.distanceTo(p2);
                mid.setLength(baseRadius + dist * 0.28);

                const curve = new THREE.QuadraticBezierCurve3(p1, mid, p2);
                const pts = curve.getPoints(32);
                const geo = new THREE.BufferGeometry().setFromPoints(pts);
                const mat = new THREE.LineBasicMaterial({{ color: 0x00f0ff, transparent: true, opacity: 0.75, blending: THREE.AdditiveBlending }});
                globeGroup.add(new THREE.Line(geo, mat));
            }}

            addTradeArc(hubs[0], hubs[1]);
            addTradeArc(hubs[0], hubs[2]);
            addTradeArc(hubs[0], hubs[3]);
            addTradeArc(hubs[0], hubs[4]);

            // 스크롤 감지
            window.addEventListener('scroll', () => {{
                const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
                scrollYProgress = Math.max(0, Math.min(1, window.scrollY / (maxScroll || 1)));
            }});

            window.addEventListener('resize', () => {{
                globeCamera.aspect = window.innerWidth / window.innerHeight;
                globeCamera.updateProjectionMatrix();
                globeRenderer.setSize(window.innerWidth, window.innerHeight);
            }});

            let clock = new THREE.Clock();

            // 렌더 루프: 영상의 HUD 눈금 및 오비탈 다층 회전 루핑 애니메이션
            function animate() {{
                requestAnimationFrame(animate);
                const time = clock.getElapsedTime();

                // 1. 지구본 자전
                continentMesh.rotation.y = time * 0.16;

                // 2. HUD 눈금 링 역방향 고속 회전
                hudTickRing.rotation.z = -time * 0.25;

                // 3. 오비탈 궤도 링 교차 회전
                hudRing1.rotation.z = time * 0.14;
                hudRing2.rotation.z = -time * 0.10;

                // 4. 브래킷 조준선 부드러운 펄스 회전
                hudBrackets.rotation.z = Math.sin(time * 0.5) * 0.15;

                // 5. 스크롤 줌인 & 공간 이동 (Scrollytelling)
                const targetX = scrollYProgress * 36;
                const targetY = -scrollYProgress * 6;
                const targetScale = 1.0 + scrollYProgress * 0.35;

                globeGroup.position.x += (targetX - globeGroup.position.x) * 0.08;
                globeGroup.position.y += (targetY - globeGroup.position.y) * 0.08;
                globeGroup.scale.set(targetScale, targetScale, targetScale);

                globeRenderer.render(globeScene, globeCamera);
            }}
            animate();
        }}
        init3DGlobe();

        // 5. 챗봇
        function toggleChatbot() {{
            const win = document.getElementById('chatbot-window');
            win.classList.toggle('hidden');
            if(!win.classList.contains('hidden')) {{ document.getElementById('chat-input').focus(); }}
        }}
        function appendMessage(text, isUser = false) {{
            const msgBox = document.getElementById('chat-messages');
            const wrap = document.createElement('div');
            wrap.className = isUser ? "flex justify-end" : "flex items-start gap-2";
            wrap.innerHTML = `<div class="${{isUser ? 'chat-bubble-user' : 'chat-bubble-ai'}} p-3 max-w-[80%] text-xs">${{text}}</div>`;
            msgBox.appendChild(wrap);
            msgBox.scrollTop = msgBox.scrollHeight;
        }}
        function askPreset(query) {{
            document.getElementById('chat-input').value = query;
            handleChatSubmit(new Event('submit'));
        }}
        function handleChatSubmit(e) {{
            e.preventDefault();
            const inp = document.getElementById('chat-input');
            const q = inp.value.trim();
            if(!q) return;
            appendMessage(q, true);
            inp.value = '';
            setTimeout(() => {{
                let ans = "해당 품목의 기술 제원을 입력해주시면 정밀 라이선스 요건을 시뮬레이션해 드립니다.";
                if(q.includes("3A090") || q.includes("통제선")) {{
                    ans = "<b>미 상무부 ECCN 3A090 규제 안내:</b><br>• TPP 4800 이상 칩은 사전 라이선스 의무화<br>• 7nm 이하 미세공정 해당 시 자동 -15점 감점";
                }} else if(q.includes("RVC") || q.includes("원산지")) {{
                    ans = "<b>RVC(역내부가가치비율) 산출:</b><br>• 기준: 55.0% 이상 확보 필수<br>• 55% 미달 시 -20점 감점 처리";
                }} else if(q.includes("HBM")) {{
                    ans = "<b>HBM3e 대미 수출 가이드:</b><br>1. 최종 사용자 서약서(End-User Statement) 필수<br>2. 동남아 우회 패키징 시 재수출 규제(FDPR) 사전 점검";
                }}
                appendMessage(ans, false);
            }}, 500);
        }}

        // 6. macOS 윈도우 드래그 & 리사이즈
        let highestZ = 30;
        function setupWindows() {{
            document.querySelectorAll('.mac-window').forEach(win => {{
                const header = win.querySelector('.window-drag-header');
                let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
                win.addEventListener('mousedown', () => {{ highestZ++; win.style.zIndex = highestZ; }});
                if(header) {{
                    header.onmousedown = function(e) {{
                        e.preventDefault();
                        highestZ++;
                        win.style.zIndex = highestZ;
                        pos3 = e.clientX; pos4 = e.clientY;
                        document.onmouseup = () => {{ document.onmouseup = null; document.onmousemove = null; }};
                        document.onmousemove = (ev) => {{
                            ev.preventDefault();
                            pos1 = pos3 - ev.clientX; pos2 = pos4 - ev.clientY;
                            pos3 = ev.clientX; pos4 = ev.clientY;
                            win.style.top = (win.offsetTop - pos2) + "px";
                            win.style.left = (win.offsetLeft - pos1) + "px";
                        }};
                    }};
                }}
            }});
        }}
        setupWindows();

        function toggleMacWindow(winId) {{
            const win = document.getElementById(winId);
            win.style.display = (win.style.display === 'none') ? 'block' : 'none';
        }}

        // 7. 차트 렌더링
        let chartTimeline = null, chartPie = null;
        function initOrUpdateCharts() {{
            const ctxTimeline = document.getElementById('chart-timeline');
            const ctxPie = document.getElementById('chart-pie');
            if(!ctxTimeline || !ctxPie) return;
            if(chartTimeline) chartTimeline.destroy();
            if(chartPie) chartPie.destroy();

            chartTimeline = new Chart(ctxTimeline, {{
                type: 'line',
                data: {{
                    labels: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월'],
                    datasets: [{{
                        label: '수출액 ($B)',
                        data: [9.2, 9.8, 10.4, 10.1, 11.2, 11.8, 12.3, 12.5, 12.8],
                        borderColor: '#00f0ff',
                        backgroundColor: 'rgba(0, 240, 255, 0.15)',
                        fill: true,
                        tension: 0.3
                    }}]
                }},
                options: {{ responsive: true, maintainAspectRatio: false }}
            }});

            chartPie = new Chart(ctxPie, {{
                type: 'doughnut',
                data: {{
                    labels: ['아시아', '북미', '유럽', '기타'],
                    datasets: [{{
                        data: [42, 28, 15, 15],
                        backgroundColor: ['#00f0ff', '#38bdf8', '#818cf8', '#cbd5e1']
                    }}]
                }},
                options: {{ responsive: true, maintainAspectRatio: false }}
            }});
        }}

        // 8. 샘플 다운로드
        function downloadSampleCSV() {{
            const csvContent = "HS_CODE,PRODUCT_NAME,PROCESS_NODE_NM,TARGET_COUNTRY,UNIT_PRICE_USD,RVC_PERCENT,ECCN_FLAG\\n" +
                               "8542.31.1000,AI 가속기 HBM3e,4,미국,2850.0,68.5,3A090\\n" +
                               "8542.32.0000,서버용 DDR5 DRAM,12,대만,145.0,62.0,None\\n" +
                               "8542.39.0000,전력반도체 SiC 모듈,45,베트남,45.0,58.0,None\\n" +
                               "8542.31.9000,차량용 제어 MCU,28,독일,85.0,71.2,None";
            const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url; a.download = "axport_semiconductor_sample.csv"; a.click();
            URL.revokeObjectURL(url);
        }}

        // 9. 파일 파싱 & 테이블 렌더링
        const initialDummyRows = [
            {{ hs: "8542.31.1000", name: "AI 가속기 HBM3e", node: 4, country: "미국", price: 2850, rvc: 68.5, eccn: "3A090" }},
            {{ hs: "8542.32.0000", name: "서버용 DDR5 DRAM", node: 12, country: "대만", price: 145, rvc: 62.0, eccn: "None" }},
            {{ hs: "8542.39.0000", name: "전력반도체 SiC 모듈", node: 45, country: "베트남", price: 45, rvc: 58.0, eccn: "None" }}
        ];

        function renderTableRows(rows) {{
            const tbody = document.getElementById('diagnosis-tbody');
            if(!tbody) return;
            tbody.innerHTML = '';
            rows.forEach(r => {{
                let score = 100;
                let reasons = [];
                if(r.node <= 7 || r.eccn === "3A090") {{
                    score -= 15;
                    reasons.push("3A090 규제군 및 미세공정(≤7nm) 해당 (-15점)");
                }}
                if(r.rvc < 55.0) {{
                    score -= 20;
                    reasons.push("RVC 55% 미달 (-20점)");
                }}
                const badgeColor = score >= 80 ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300" : "bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300";
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td class="p-3 font-mono">${{r.hs}}</td>
                    <td class="p-3 font-bold">${{r.name}}</td>
                    <td class="p-3">${{r.node}} nm</td>
                    <td class="p-3">${{r.country}}</td>
                    <td class="p-3">$${{Number(r.price).toLocaleString()}}</td>
                    <td class="p-3">${{r.rvc}}%</td>
                    <td class="p-3"><span class="px-2.5 py-1 rounded-full text-xs font-bold ${{badgeColor}}">${{score}}점</span></td>
                    <td class="p-3 text-slate-500 dark:text-slate-400">${{reasons.length ? reasons.join(" / ") : "만점 통과"}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}
        renderTableRows(initialDummyRows);

        function handleFileUpload(e) {{
            const file = e.target.files[0];
            if(!file) return;
            const reader = new FileReader();
            reader.onload = function(evt) {{
                const lines = evt.target.result.split('\\n').filter(l => l.trim().length > 0);
                const parsed = [];
                for(let i = 1; i < lines.length; i++) {{
                    const cols = lines[i].split(',');
                    if(cols.length >= 6) {{
                        parsed.push({{
                            hs: cols[0].trim(),
                            name: cols[1].trim(),
                            node: parseInt(cols[2]) || 28,
                            country: cols[3].trim(),
                            price: parseFloat(cols[4]) || 100,
                            rvc: parseFloat(cols[5]) || 60,
                            eccn: cols[6] ? cols[6].trim() : "None"
                        }});
                    }}
                }}
                if(parsed.length) {{
                    renderTableRows(parsed);
                    alert("성공적으로 " + parsed.length + "건의 데이터를 분석했습니다.");
                }}
            }};
            reader.readAsText(file);
        }}
    </script>
</body>
</html>
"""

# Streamlit 풀스크린 임베딩
components.html(raw_html, height=1000, scrolling=True)