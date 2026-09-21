import os
import base64
import streamlit as st
import streamlit.components.v1 as components

# 1. Streamlit 페이지 설정
st.set_page_config(
    page_title="Axport - Semiconductor Trade Intelligence",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Streamlit 기본 여백 제거
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

# 3. 로컬 및 Streamlit Cloud 겸용 상대 경로 Base64 변환
def get_image_base64(filename):
    candidates = [
        filename,
        os.path.join(os.path.dirname(__file__), filename) if '__file__' in globals() else filename,
        os.path.join(r"C:\Users\user\Desktop\axport_demo_gemini", filename)
    ]
    for p in candidates:
        if p and os.path.exists(p):
            try:
                with open(p, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode()
                    ext = os.path.splitext(p)[1].lower().replace('.', '')
                    mime = 'image/svg+xml' if ext == 'svg' else ('image/jpeg' if ext in ['jpg', 'jpeg'] else 'image/png')
                    return f"data:{mime};base64,{encoded}"
            except Exception:
                pass
    return ""

# Streamlit Cloud 배포를 위한 상대 파일명 설정
logo_b64 = get_image_base64("Axport_logo_png.png")
chatbot_b64 = get_image_base64("Axport_AI.png")

# 4. Orakl 스타일 스크롤리텔링 3D 인터랙션 내장 웹 앱
raw_html = f"""
<!DOCTYPE html>
<html lang="ko" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Axport - Semiconductor Trade Intelligence</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Three.js (r128) -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Inter:wght@300;400;500;600;700;800&display=swap');
        * {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }}
        
        .logo-font {{ font-family: 'Montserrat', sans-serif; font-weight: 900; }}

        .mac-glass {{
            background: rgba(255, 255, 255, 0.94);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            box-shadow: 0 20px 45px -12px rgba(0, 0, 0, 0.35);
        }}
        .mac-desktop-bg {{
            background: radial-gradient(circle at 50% 20%, #1e3a8a 0%, #0f172a 60%, #020617 100%);
        }}

        /* 윈도우 실제 크기 조절(Resizable) */
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

        /* 챗봇 스타일 */
        .chatbot-container {{ box-shadow: 0 24px 48px -12px rgba(15, 23, 42, 0.35); }}
        .chat-bubble-ai {{ background: #F1F5F9; color: #0F172A; border-radius: 16px 16px 16px 4px; }}
        .chat-bubble-user {{ background: #2563EB; color: #FFFFFF; border-radius: 16px 16px 4px 16px; }}

        ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        ::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 4px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
    </style>
</head>
<body class="bg-[#030712] text-slate-100 antialiased overflow-x-hidden min-h-screen selection:bg-blue-600 selection:text-white">

    <!-- 상단 글로벌 고정 헤더 -->
    <header class="fixed top-0 left-0 right-0 z-50 bg-[#030712]/80 backdrop-blur-lg border-b border-slate-800/80 transition-all duration-300">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center gap-6">
                <!-- Axport 로고 -->
                <div class="cursor-pointer flex items-center select-none" onclick="switchView('landing')">
                    <img id="header-logo-img" src="{logo_b64}" alt="AXPORT" class="h-10 object-contain" onerror="this.style.display='none'; document.getElementById('header-logo-fallback').style.display='block';" />
                    <div id="header-logo-fallback" class="hidden">
                        <span class="text-2xl font-black tracking-widest text-white">AXPORT</span>
                    </div>
                </div>

                <!-- 네비게이션 버튼 -->
                <nav class="hidden md:flex items-center gap-1 bg-slate-900/90 p-1 rounded-xl border border-slate-800">
                    <button onclick="switchView('landing')" id="nav-landing" class="px-4 py-1.5 rounded-lg text-sm font-semibold transition-all bg-blue-600 text-white shadow-sm">홈 (스토리텔링)</button>
                    <button onclick="switchView('dashboard')" id="nav-dashboard" class="px-4 py-1.5 rounded-lg text-sm font-medium text-slate-400 hover:text-white transition-all">메인 대시보드</button>
                    <button onclick="switchView('custom-mac')" id="nav-custom-mac" class="px-4 py-1.5 rounded-lg text-sm font-medium text-slate-400 hover:text-white flex items-center gap-1.5 transition-all">
                        <i data-lucide="layout-grid" class="w-4 h-4"></i> 사용자 커스텀 뷰
                    </button>
                </nav>
            </div>

            <!-- 우측 컨트롤러 -->
            <div class="flex items-center gap-3">
                <button onclick="toggleChatbot()" class="flex items-center gap-1.5 bg-blue-950/80 hover:bg-blue-900 text-blue-400 text-xs font-bold px-3 py-1.5 rounded-lg border border-blue-800/60 transition-all">
                    <i data-lucide="bot" class="w-4 h-4 text-blue-400"></i> Axport AI 챗봇
                </button>
                <div class="flex items-center bg-slate-900/90 rounded-lg p-1 text-xs font-semibold border border-slate-800">
                    <button id="curr-usd" onclick="setCurrency('USD')" class="px-2.5 py-1 rounded-md bg-blue-600 text-white shadow-xs">USD ($)</button>
                    <button id="curr-krw" onclick="setCurrency('KRW')" class="px-2.5 py-1 rounded-md text-slate-400 hover:text-white">KRW (₩)</button>
                </div>
            </div>
        </div>
    </header>

    <!-- ================= VIEW 1: Orakl 스타일 스크롤 연동 3D 지구본 (Scrollytelling) ================= -->
    <section id="view-landing" class="relative block w-full bg-[#030712]">
        
        <!-- 고정 3D 캔버스 컨테이너 (스크롤 시 배경에 고정되어 모션 변화) -->
        <div id="canvas-sticky-wrap" class="fixed inset-0 z-0 pointer-events-none w-full h-full">
            <div id="globe-container" class="w-full h-full"></div>
        </div>

        <!-- 1단계: 진입 히어로 (중앙 구체에서 꿈틀거리는 데이터 파동 감상) -->
        <div class="relative z-10 min-h-screen flex flex-col items-center justify-center text-center px-4 pt-16">
            <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold backdrop-blur-md mb-6 animate-pulse">
                <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
                Cybernetic Trade Intelligence Engine
            </div>
            <h1 class="text-4xl sm:text-7xl font-black tracking-tight text-white max-w-4xl leading-tight">
                반도체 수출 적합성의 <br>
                <span class="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-500 to-indigo-400">새로운 지평, Axport</span>
            </h1>
            <p class="mt-6 text-slate-400 text-sm sm:text-lg max-w-xl leading-relaxed">
                살아 움직이는 글로벌 무역망 데이터를 스크롤하여 탐험하세요.
            </p>
            <div class="flex gap-4 mt-8 pointer-events-auto">
                <button onclick="switchView('dashboard')" class="bg-blue-600 hover:bg-blue-500 text-white font-bold px-6 py-3 rounded-xl shadow-lg shadow-blue-600/30 transition-all flex items-center gap-2 text-sm">
                    <i data-lucide="gauge" class="w-4 h-4"></i> 메인 대시보드 바로가기
                </button>
            </div>
        </div>

        <!-- 2단계: 스크롤을 내리면 지구가 줌인되며 나타나는 회사 소개 (Orakl 스타일 전환) -->
        <div class="relative z-10 min-h-screen flex items-center px-6 sm:px-16 py-24">
            <div class="max-w-xl bg-slate-950/75 backdrop-blur-xl p-8 sm:p-10 rounded-3xl border border-slate-800/80 shadow-2xl space-y-5">
                <div class="text-xs font-bold uppercase tracking-widest text-cyan-400">About Axport</div>
                <h2 class="text-2xl sm:text-4xl font-extrabold text-white leading-tight">
                    복잡한 통제 규제를 <br>단 하나의 흐름으로
                </h2>
                <p class="text-slate-300 text-sm leading-relaxed">
                    반도체 공급망은 멈추지 않는 유기체와 같습니다. Axport는 기업 내부의 원시 데이터(Raw CSV/ERP)를 실시간으로 스트리밍하여, 미 상무부 BIS 수출통제(ECCN 3A090)와 원산지 부가가치기준(RVC)을 완전 자동으로 판정합니다.
                </p>
                <div class="pt-2 flex items-center gap-6">
                    <div>
                        <div class="text-2xl font-black text-cyan-400">99.8%</div>
                        <div class="text-xs text-slate-400">규제 판정 정확도</div>
                    </div>
                    <div class="w-px h-8 bg-slate-800"></div>
                    <div>
                        <div class="text-2xl font-black text-blue-400">Zero-ETL</div>
                        <div class="text-xs text-slate-400">무가공 자동 전처리</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 3단계: 핵심 강점 카드 섹션 -->
        <div class="relative z-10 max-w-7xl mx-auto px-6 py-24">
            <div class="text-center max-w-2xl mx-auto mb-16">
                <h3 class="text-xs font-bold uppercase tracking-wider text-cyan-400 mb-2">Core Advantages</h3>
                <h4 class="text-3xl font-extrabold text-white">Axport만의 3단계 적합성 파이프라인</h4>
            </div>
            <div class="grid md:grid-cols-3 gap-6">
                <div class="bg-slate-900/80 backdrop-blur-md p-8 rounded-2xl border border-slate-800/80 hover:border-blue-500/50 transition-all group">
                    <div class="w-12 h-12 rounded-xl bg-blue-500/10 text-cyan-400 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                        <i data-lucide="database" class="w-6 h-6"></i>
                    </div>
                    <h5 class="text-lg font-bold text-white mb-2">1. 원클릭 Zero-ETL</h5>
                    <p class="text-slate-400 text-xs leading-relaxed">기업마다 제각각인 ERP 인보이스 CSV를 올리기만 하면 통화 환산과 결측치를 알아서 정규화합니다.</p>
                </div>
                <div class="bg-slate-900/80 backdrop-blur-md p-8 rounded-2xl border border-slate-800/80 hover:border-blue-500/50 transition-all group">
                    <div class="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                        <i data-lucide="shield-check" class="w-6 h-6"></i>
                    </div>
                    <h5 class="text-lg font-bold text-white mb-2">2. 투명한 감점 원인 역추적</h5>
                    <p class="text-slate-400 text-xs leading-relaxed">왜 점수가 감점되었는지(ECCN 3A090 통제선, RVC 부가가치 미달)를 명확히 제시하며 담당자가 검수할 수 있습니다.</p>
                </div>
                <div class="bg-slate-900/80 backdrop-blur-md p-8 rounded-2xl border border-slate-800/80 hover:border-blue-500/50 transition-all group">
                    <div class="w-12 h-12 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                        <i data-lucide="activity" class="w-6 h-6"></i>
                    </div>
                    <h5 class="text-lg font-bold text-white mb-2">3. 실시간 매크로 헤징</h5>
                    <p class="text-slate-400 text-xs leading-relaxed">실시간 주요국 환율, DRAM 현물 가격, 대상국 세관 보류율을 동기화하여 환차손과 물류 병목을 방지합니다.</p>
                </div>
            </div>
            
            <div class="text-center mt-16 pb-12">
                <button onclick="switchView('dashboard')" class="bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-bold px-8 py-4 rounded-2xl shadow-xl shadow-cyan-500/20 transition-all">
                    지금 대시보드에서 데이터 진단하기 →
                </button>
            </div>
        </div>
    </section>

    <!-- ================= VIEW 2: 메인 기본 대시보드 ================= -->
    <section id="view-dashboard" class="hidden bg-[#F8FAFC] text-slate-800 min-h-screen pt-20 px-4 sm:px-6 lg:px-8 pb-16 space-y-6">
        <div class="max-w-7xl mx-auto space-y-6">
            <div class="flex items-center justify-between border-b border-slate-200 pb-3">
                <div class="flex items-center gap-2 sm:gap-4 overflow-x-auto">
                    <button onclick="switchDashTab('tab-summary')" id="btntab-summary" class="dash-tab-btn px-4 py-2 text-sm font-bold border-b-2 border-blue-600 text-blue-600">📊 종합 요약</button>
                    <button onclick="switchDashTab('tab-upload')" id="btntab-upload" class="dash-tab-btn px-4 py-2 text-sm font-medium text-slate-500 hover:text-slate-900 border-b-2 border-transparent">🔍 데이터 업로드 & 진단</button>
                    <button onclick="switchDashTab('tab-criteria')" id="btntab-criteria" class="dash-tab-btn px-4 py-2 text-sm font-medium text-slate-500 hover:text-slate-900 border-b-2 border-transparent">📋 평가 기준 및 배점표</button>
                    <button onclick="switchDashTab('tab-risks')" id="btntab-risks" class="dash-tab-btn px-4 py-2 text-sm font-medium text-slate-500 hover:text-slate-900 border-b-2 border-transparent">🛡️ 규제/통관 리스크</button>
                    <button onclick="switchDashTab('tab-macro')" id="btntab-macro" class="dash-tab-btn px-4 py-2 text-sm font-medium text-slate-500 hover:text-slate-900 border-b-2 border-transparent">📈 시황 & 환율</button>
                </div>
                <button onclick="switchView('custom-mac')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-all">
                    <i data-lucide="layers" class="w-3.5 h-3.5"></i> 커스텀 뷰 모드로 전환
                </button>
            </div>

            <!-- 탭 1: 종합 요약 -->
            <div id="content-tab-summary" class="space-y-6">
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div class="kpi-gradient-blue p-5 rounded-2xl text-white shadow-sm">
                        <div class="text-xs font-semibold uppercase tracking-wider opacity-85">총 수출액 (SEMICON)</div>
                        <div class="text-3xl font-extrabold mt-2 kpi-val" data-usd="12.8" data-unit="B">$12.8B</div>
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
                        <div class="text-3xl font-extrabold mt-2 kpi-val" data-usd="3.4" data-unit="B">$3.4B</div>
                        <div class="text-xs mt-2 inline-flex items-center gap-1 bg-white/20 px-2.5 py-0.5 rounded-full font-medium">▲ 6.1% 전월 대비</div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="lg:col-span-2 bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">
                        <div class="flex items-center justify-between mb-4">
                            <h4 class="font-bold text-slate-800 text-sm flex items-center gap-2">
                                <i data-lucide="trending-up" class="w-4 h-4 text-blue-600"></i> 월별 반도체 수출 추이 (YoY)
                            </h4>
                            <span class="text-xs text-slate-400">단위: Billion USD</span>
                        </div>
                        <div class="h-64 relative"><canvas id="chart-timeline"></canvas></div>
                    </div>
                    <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">
                        <div class="flex items-center justify-between mb-4">
                            <h4 class="font-bold text-slate-800 text-sm flex items-center gap-2">
                                <i data-lucide="pie-chart" class="w-4 h-4 text-blue-600"></i> 주요국 수출 점유율
                            </h4>
                        </div>
                        <div class="h-64 relative flex items-center justify-center"><canvas id="chart-pie"></canvas></div>
                    </div>
                </div>
                
                <div class="bg-blue-50 border border-blue-200 rounded-xl p-4 text-blue-900 text-xs leading-relaxed flex items-start gap-3">
                    <i data-lucide="info" class="w-5 h-5 text-blue-600 shrink-0 mt-0.5"></i>
                    <div>
                        <b>[시장 시사점 도출]</b> AI 가속기 및 HBM3e 중심의 고부가 패키징 수출 수요 확대로 대미 수출 점유율이 28%로 견고하게 유지되고 있습니다. 다만, 미 상무부 BIS의 첨단 컴퓨팅 칩(ECCN 3A090) 수출통제 개정으로 인해 동남아 우회 통관 시 최종 사용자(End-User) 검증 서약 절차를 보강할 필요가 있습니다.
                    </div>
                </div>
            </div>

            <!-- 탭 2: 데이터 업로드 & 진단 엔진 -->
            <div id="content-tab-upload" class="hidden space-y-6">
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                        <div>
                            <h3 class="text-lg font-bold text-slate-900">반도체 원시 데이터(Raw File) 자동 전처리 및 평가</h3>
                            <p class="text-xs text-slate-500 mt-1">기업의 비정형 CSV 데이터를 업로드하면 결측치 보간, USD 환산 및 100점 만점 적합도를 즉시 산출합니다.</p>
                        </div>
                        <button onclick="downloadSampleCSV()" class="bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs px-4 py-2.5 rounded-xl flex items-center gap-2 transition-all shrink-0">
                            <i data-lucide="download" class="w-4 h-4 text-blue-600"></i> 필수 항목 샘플(.csv) 다운로드
                        </button>
                    </div>

                    <div class="border-2 border-dashed border-slate-300 hover:border-blue-500 rounded-2xl p-8 text-center transition-all cursor-pointer bg-slate-50/50" onclick="document.getElementById('file-input').click()">
                        <input type="file" id="file-input" class="hidden" accept=".csv" onchange="handleFileUpload(event)">
                        <i data-lucide="upload-cloud" class="w-10 h-10 text-blue-600 mx-auto mb-2"></i>
                        <p class="text-sm font-semibold text-slate-700">여기를 클릭하거나 CSV 파일을 드래그하여 업로드하세요</p>
                        <p class="text-xs text-slate-400 mt-1">지원 형식: .csv (HS_CODE, PRODUCT_NAME, PROCESS_NODE_NM, TARGET_COUNTRY 필수 포함)</p>
                    </div>
                </div>

                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
                    <div class="flex items-center justify-between">
                        <div>
                            <h4 class="font-bold text-slate-900 text-base">품목별 수출 적합성 진단 결과</h4>
                            <p class="text-xs text-slate-500">평가 기준표에 따른 자동 감점 및 합격 여부 판정 내역</p>
                        </div>
                        <div class="text-right">
                            <span class="text-xs text-slate-400">평균 적합도</span>
                            <div class="text-2xl font-black text-emerald-600" id="total-score-badge">88.5점 (적합)</div>
                        </div>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-xs border-collapse">
                            <thead>
                                <tr class="bg-slate-100 text-slate-600 font-semibold border-b border-slate-200">
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
                            <tbody id="diagnosis-tbody" class="divide-y divide-slate-100"></tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- 탭 3: 평가 기준 및 배점표 -->
            <div id="content-tab-criteria" class="hidden space-y-6">
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-6">
                    <div class="border-b border-slate-200 pb-4">
                        <h3 class="text-lg font-bold text-slate-900">⚖️ Axport 반도체 수출 적합성 평가 기준 및 배점 체계</h3>
                        <p class="text-xs text-slate-500 mt-1">국제 전략물자 통제 조약(바세나르 협정), 미 상무부 수출관리규정(EAR), 그리고 자유무역협정(FTA) 원산지 기준에 기반합니다.</p>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div class="p-4 rounded-xl border border-blue-200 bg-blue-50/50">
                            <div class="flex justify-between items-center mb-1">
                                <span class="text-xs font-bold text-blue-800">1. 기술 규제 적합도</span>
                                <span class="text-xs bg-blue-200 text-blue-900 px-2 py-0.5 rounded-full font-extrabold">35점 배점</span>
                            </div>
                            <p class="text-[11px] text-slate-600 mt-2 leading-relaxed">• ECCN 3A090 통제선 미달 여부<br>• 웨이퍼 미세공정 (≤ 7nm 감점)<br>• TPP 연산능력 밀도 분석</p>
                        </div>
                        <div class="p-4 rounded-xl border border-emerald-200 bg-emerald-50/50">
                            <div class="flex justify-between items-center mb-1">
                                <span class="text-xs font-bold text-emerald-800">2. 원산지 기준 충족도</span>
                                <span class="text-xs bg-emerald-200 text-emerald-900 px-2 py-0.5 rounded-full font-extrabold">30점 배점</span>
                            </div>
                            <p class="text-[11px] text-slate-600 mt-2 leading-relaxed">• 역내부가가치비율(RVC) 산출<br>• RVC 55% 이상: 만점<br>• 세번변경기준(CTSH) 충족성</p>
                        </div>
                        <div class="p-4 rounded-xl border border-amber-200 bg-amber-50/50">
                            <div class="flex justify-between items-center mb-1">
                                <span class="text-xs font-bold text-amber-800">3. 세관 통관 리스크</span>
                                <span class="text-xs bg-amber-200 text-amber-900 px-2 py-0.5 rounded-full font-extrabold">20점 배점</span>
                            </div>
                            <p class="text-[11px] text-slate-600 mt-2 leading-relaxed">• 대상국 세관 평균 보류율<br>• 최종 사용자(End-User) 신뢰도<br>• 우회 수출 경로 점검</p>
                        </div>
                        <div class="p-4 rounded-xl border border-purple-200 bg-purple-50/50">
                            <div class="flex justify-between items-center mb-1">
                                <span class="text-xs font-bold text-purple-800">4. 시장 및 가격 경쟁력</span>
                                <span class="text-xs bg-purple-200 text-purple-900 px-2 py-0.5 rounded-full font-extrabold">15점 배점</span>
                            </div>
                            <p class="text-[11px] text-slate-600 mt-2 leading-relaxed">• 글로벌 DRAM/NAND 단가 추이<br>• 원/달러 환율 민감도 변동폭<br>• 인보이스 가격 적정성</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 탭 4: 규제 & 통관 리스크 -->
            <div id="content-tab-risks" class="hidden space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-white p-6 rounded-2xl border border-slate-200">
                        <h4 class="font-bold text-slate-900 text-sm mb-4">미국 상무부 BIS 핵심 ECCN 통제 기준</h4>
                        <div class="space-y-3 text-xs">
                            <div class="p-3 bg-red-50 border-l-4 border-red-500 rounded-r-lg">
                                <div class="font-bold text-red-900">ECCN 3A090.a (첨단 가속기 칩)</div>
                                <p class="text-red-700 mt-1">Total Processing Performance >= 4800 조항 해당 시 라이선스 발급 의무화</p>
                            </div>
                            <div class="p-3 bg-amber-50 border-l-4 border-amber-500 rounded-r-lg">
                                <div class="font-bold text-amber-900">ECCN 3A090.b (성능 밀도 칩)</div>
                                <p class="text-amber-700 mt-1">Performance Density 조항 충족 시 사전 통보(NAC) 절차 필수</p>
                            </div>
                            <div class="p-3 bg-emerald-50 border-l-4 border-emerald-500 rounded-r-lg">
                                <div class="font-bold text-emerald-900">EAR99 (범용 반도체)</div>
                                <p class="text-emerald-700 mt-1">일반 메모리 및 성숙 공정(28nm 이상) 부품으로 통관 리스크 없음</p>
                            </div>
                        </div>
                    </div>
                    <div class="bg-white p-6 rounded-2xl border border-slate-200">
                        <h4 class="font-bold text-slate-900 text-sm mb-4">주요 수출 대상국별 세관 정밀 검사율</h4>
                        <div class="space-y-4">
                            <div>
                                <div class="flex justify-between text-xs font-semibold mb-1">
                                    <span>미국 (CBP)</span><span class="text-slate-600">2.8% (양호)</span>
                                </div>
                                <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                                    <div class="bg-blue-600 h-full w-[28%]"></div>
                                </div>
                            </div>
                            <div>
                                <div class="flex justify-between text-xs font-semibold mb-1">
                                    <span>대만 (신주 FAB 경유)</span><span class="text-slate-600">1.4% (매우 양호)</span>
                                </div>
                                <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                                    <div class="bg-emerald-500 h-full w-[14%]"></div>
                                </div>
                            </div>
                            <div>
                                <div class="flex justify-between text-xs font-semibold mb-1">
                                    <span>중국 (세관 총서)</span><span class="text-red-600 font-bold">12.4% (정밀 검사 주의)</span>
                                </div>
                                <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                                    <div class="bg-red-500 h-full w-[80%]"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 탭 5: 시황 & 환율 -->
            <div id="content-tab-macro" class="hidden space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="bg-white p-5 rounded-2xl border border-slate-200">
                        <span class="text-xs text-slate-500">실시간 환율 (KEB하나)</span>
                        <div class="text-2xl font-bold text-slate-900 mt-1">1,350.20 원</div>
                        <span class="text-xs text-red-500 font-medium">▲ 3.20 (0.24%)</span>
                    </div>
                    <div class="bg-white p-5 rounded-2xl border border-slate-200">
                        <span class="text-xs text-slate-500">DRAM DXI 현물 지수</span>
                        <div class="text-2xl font-bold text-slate-900 mt-1">28,450</div>
                        <span class="text-xs text-emerald-600 font-medium">▲ 1.4% 전일비</span>
                    </div>
                    <div class="bg-white p-5 rounded-2xl border border-slate-200">
                        <span class="text-xs text-slate-500">반도체 운임 지수 (SCFI)</span>
                        <div class="text-2xl font-bold text-slate-900 mt-1">1,940 pt</div>
                        <span class="text-xs text-blue-600 font-medium">안정세 유지</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- ================= VIEW 3: 사용자 커스텀 뷰 (macOS 스타일) ================= -->
    <section id="view-custom-mac" class="hidden relative w-full h-[92vh] pt-16 mac-desktop-bg overflow-hidden">
        <div class="absolute top-20 left-1/2 -translate-x-1/2 z-50 flex items-center gap-2 bg-white/20 backdrop-blur-xl border border-white/30 px-4 py-2 rounded-2xl shadow-xl">
            <button onclick="toggleMacWindow('mac-win1')" id="btn-win1" class="px-3.5 py-1.5 rounded-xl text-xs font-semibold text-white bg-blue-600 shadow-md flex items-center gap-1.5 transition-all">
                <i data-lucide="bar-chart-2" class="w-3.5 h-3.5"></i> KPI 요약 창
            </button>
            <button onclick="toggleMacWindow('mac-win2')" id="btn-win2" class="px-3.5 py-1.5 rounded-xl text-xs font-semibold text-white bg-blue-600 shadow-md flex items-center gap-1.5 transition-all">
                <i data-lucide="shield-check" class="w-3.5 h-3.5"></i> 기업 적합도 판정 창
            </button>
            <button onclick="toggleMacWindow('mac-win3')" id="btn-win3" class="px-3.5 py-1.5 rounded-xl text-xs font-semibold text-white bg-blue-600 shadow-md flex items-center gap-1.5 transition-all">
                <i data-lucide="alert-triangle" class="w-3.5 h-3.5"></i> 규제 리스크 창
            </button>
            <button onclick="toggleMacWindow('mac-win4')" id="btn-win4" class="px-3.5 py-1.5 rounded-xl text-xs font-semibold text-white bg-blue-600 shadow-md flex items-center gap-1.5 transition-all">
                <i data-lucide="trending-up" class="w-3.5 h-3.5"></i> 환율 & 시황 창
            </button>
        </div>

        <!-- 윈도우 1: KPI 요약 -->
        <div id="mac-win1" class="mac-window w-80 mac-glass rounded-2xl shadow-2xl" style="top: 120px; left: 40px; z-index: 20;">
            <div class="window-drag-header bg-slate-100/70 border-b border-slate-200/50 px-3.5 py-2.5 flex items-center justify-between">
                <div class="flex items-center gap-1.5">
                    <span class="w-3 h-3 rounded-full bg-red-400 cursor-pointer" onclick="toggleMacWindow('mac-win1')"></span>
                    <span class="w-3 h-3 rounded-full bg-amber-400"></span>
                    <span class="w-3 h-3 rounded-full bg-emerald-400"></span>
                </div>
                <span class="text-xs font-semibold text-slate-700">SEMICON KPI 요약</span>
                <div class="w-6"></div>
            </div>
            <div class="p-4 space-y-3">
                <div class="p-3 rounded-xl bg-blue-50/80 border border-blue-100">
                    <span class="text-[11px] font-bold text-blue-600 uppercase">총 수출액</span>
                    <div class="text-2xl font-black text-blue-900">$12.8B</div>
                    <span class="text-[11px] text-emerald-600 font-semibold">▲ 8.4% 전월 대비</span>
                </div>
                <div class="text-xs text-slate-600 space-y-1">
                    <div class="flex justify-between"><span>생산 가동률:</span><b>92.1%</b></div>
                    <div class="flex justify-between"><span>글로벌 수요:</span><b>118.4 pt</b></div>
                    <div class="flex justify-between"><span>신규 수주:</span><b>$3.4B</b></div>
                </div>
            </div>
        </div>

        <!-- 윈도우 2: 기업 적합도 판정 -->
        <div id="mac-win2" class="mac-window w-96 mac-glass rounded-2xl shadow-2xl" style="top: 120px; left: 380px; z-index: 21;">
            <div class="window-drag-header bg-slate-100/70 border-b border-slate-200/50 px-3.5 py-2.5 flex items-center justify-between">
                <div class="flex items-center gap-1.5">
                    <span class="w-3 h-3 rounded-full bg-red-400 cursor-pointer" onclick="toggleMacWindow('mac-win2')"></span>
                    <span class="w-3 h-3 rounded-full bg-amber-400"></span>
                    <span class="w-3 h-3 rounded-full bg-emerald-400"></span>
                </div>
                <span class="text-xs font-semibold text-slate-700">수출 적합성 진단 엔진</span>
                <div class="w-6"></div>
            </div>
            <div class="p-4 space-y-3 text-xs">
                <div class="flex items-center justify-between pb-2 border-b border-slate-200">
                    <span class="font-bold text-slate-700">진단 종합 결과</span>
                    <span class="px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-700 font-bold">88.5점 (합격)</span>
                </div>
                <div class="space-y-1.5 text-slate-600">
                    <div class="flex justify-between"><span>• ECCN 3A090 검토:</span><b class="text-blue-600">해당 없음 (Pass)</b></div>
                    <div class="flex justify-between"><span>• 부가가치기준(RVC):</span><b class="text-blue-600">65.2% (기준 충족)</b></div>
                    <div class="flex justify-between"><span>• 세관 보류 위험:</span><b class="text-emerald-600">정상 통과</b></div>
                </div>
            </div>
        </div>

        <!-- 윈도우 3: 규제 리스크 -->
        <div id="mac-win3" class="mac-window w-84 mac-glass rounded-2xl shadow-2xl" style="top: 340px; left: 100px; z-index: 22;">
            <div class="window-drag-header bg-slate-100/70 border-b border-slate-200/50 px-3.5 py-2.5 flex items-center justify-between">
                <div class="flex items-center gap-1.5">
                    <span class="w-3 h-3 rounded-full bg-red-400 cursor-pointer" onclick="toggleMacWindow('mac-win3')"></span>
                    <span class="w-3 h-3 rounded-full bg-amber-400"></span>
                    <span class="w-3 h-3 rounded-full bg-emerald-400"></span>
                </div>
                <span class="text-xs font-semibold text-slate-700">통관 리스크 모니터</span>
                <div class="w-6"></div>
            </div>
            <div class="p-4 text-xs space-y-2">
                <div class="p-2.5 bg-amber-50 rounded-xl border border-amber-200 text-amber-900">
                    <b>⚠️ 세관 점검 권고</b><br>
                    대만 신주 FAB 경유 인보이스 건 관련 최종 사용자(End-User) 서약서 지참 필수
                </div>
            </div>
        </div>

        <!-- 윈도우 4: 환율 및 시황 -->
        <div id="mac-win4" class="mac-window w-80 mac-glass rounded-2xl shadow-2xl" style="top: 320px; left: 520px; z-index: 23;">
            <div class="window-drag-header bg-slate-100/70 border-b border-slate-200/50 px-3.5 py-2.5 flex items-center justify-between">
                <div class="flex items-center gap-1.5">
                    <span class="w-3 h-3 rounded-full bg-red-400 cursor-pointer" onclick="toggleMacWindow('mac-win4')"></span>
                    <span class="w-3 h-3 rounded-full bg-amber-400"></span>
                    <span class="w-3 h-3 rounded-full bg-emerald-400"></span>
                </div>
                <span class="text-xs font-semibold text-slate-700">FX & DRAM Spot Feed</span>
                <div class="w-6"></div>
            </div>
            <div class="p-4 text-xs space-y-2 text-slate-700">
                <div class="flex justify-between pb-1 border-b border-slate-100">
                    <span>USD / KRW</span><b>1,350.2 원 (+3.2)</b>
                </div>
                <div class="flex justify-between pb-1 border-b border-slate-100">
                    <span>DRAM DXI 현물가</span><b>$4.25 (▲ 2.1%)</b>
                </div>
                <div class="flex justify-between">
                    <span>NAND 플래시 단가</span><b>$3.10 (보합)</b>
                </div>
            </div>
        </div>
    </section>

    <!-- ================= 플로팅 AI 챗봇 컴포넌트 ================= -->
    <div id="chatbot-trigger" onclick="toggleChatbot()" class="fixed bottom-6 right-6 z-50 cursor-pointer group">
        <div class="relative w-14 h-14 rounded-full bg-blue-600 flex items-center justify-center text-white shadow-2xl hover:scale-105 transition-transform overflow-hidden border-2 border-white">
            <img src="{chatbot_b64}" alt="AI" class="w-full h-full object-cover" onerror="this.style.display='none'; document.getElementById('chat-icon-fallback').style.display='block';" />
            <div id="chat-icon-fallback" class="hidden">
                <i data-lucide="message-square" class="w-6 h-6"></i>
            </div>
            <span class="absolute top-0 right-0 w-3.5 h-3.5 rounded-full bg-emerald-400 border-2 border-white"></span>
        </div>
    </div>

    <div id="chatbot-window" class="hidden fixed bottom-24 right-6 z-50 w-96 max-w-[90vw] h-[520px] bg-white rounded-3xl border border-slate-200 chatbot-container flex flex-col overflow-hidden animate-in fade-in slide-in-from-bottom-5">
        <div class="bg-gradient-to-r from-blue-700 to-indigo-800 p-4 text-white flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-full bg-white/20 p-0.5 overflow-hidden border border-white/40">
                    <img src="{chatbot_b64}" alt="AI" class="w-full h-full object-cover rounded-full" onerror="this.src='https://api.dicebear.com/7.x/bottts/svg?seed=Axport';" />
                </div>
                <div>
                    <h4 class="font-bold text-sm leading-none flex items-center gap-1.5 text-white">
                        Axport AI 어시스턴트
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    </h4>
                    <p class="text-[11px] text-blue-200 mt-1">반도체 수출 통제 & 규제 실시간 상담</p>
                </div>
            </div>
            <button onclick="toggleChatbot()" class="text-white/80 hover:text-white p-1">
                <i data-lucide="x" class="w-5 h-5"></i>
            </button>
        </div>

        <div class="p-2.5 bg-slate-50 border-b border-slate-100 flex gap-1.5 overflow-x-auto text-[11px]">
            <button onclick="askPreset('ECCN 3A090 규제 기준이 뭐야?')" class="px-2.5 py-1 rounded-full bg-white border border-slate-200 text-slate-700 whitespace-nowrap hover:bg-blue-50 hover:text-blue-600 transition-colors">3A090 통제선</button>
            <button onclick="askPreset('RVC 부가가치기준 계산법 알려줘')" class="px-2.5 py-1 rounded-full bg-white border border-slate-200 text-slate-700 whitespace-nowrap hover:bg-blue-50 hover:text-blue-600 transition-colors">RVC 산출 공식</button>
            <button onclick="askPreset('HBM3e 대미 수출 시 주의점은?')" class="px-2.5 py-1 rounded-full bg-white border border-slate-200 text-slate-700 whitespace-nowrap hover:bg-blue-50 hover:text-blue-600 transition-colors">HBM 대미 수출</button>
        </div>

        <div id="chat-messages" class="flex-1 p-4 overflow-y-auto space-y-3 text-xs text-slate-800">
            <div class="flex items-start gap-2">
                <div class="w-7 h-7 rounded-full bg-blue-100 overflow-hidden shrink-0 mt-0.5">
                    <img src="{chatbot_b64}" alt="AI" class="w-full h-full object-cover" onerror="this.src='https://api.dicebear.com/7.x/bottts/svg?seed=Axport';" />
                </div>
                <div class="chat-bubble-ai p-3 max-w-[80%] leading-relaxed">
                    안녕하세요! <b>Axport 반도체 무역 규제 전담 AI</b>입니다.<br>
                    ECCN 전략물자 판정, RVC 원산지 비율, 수출 서류 검수 등 궁금한 점을 편하게 질문해주세요.
                </div>
            </div>
        </div>

        <div class="p-3 bg-white border-t border-slate-100">
            <form id="chat-form" onsubmit="handleChatSubmit(event)" class="flex items-center gap-2">
                <input type="text" id="chat-input" placeholder="질문을 입력하세요..." class="flex-1 bg-slate-100 border-none rounded-xl px-3.5 py-2.5 text-xs text-slate-800 focus:ring-2 focus:ring-blue-600 focus:outline-none" />
                <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white p-2.5 rounded-xl transition-all shadow-sm">
                    <i data-lucide="send" class="w-4 h-4"></i>
                </button>
            </form>
        </div>
    </div>

    <!-- JS 스크립트: Orakl 스타일 유기적 펄스 & 스크롤 연동 3D 엔진 -->
    <script>
        lucide.createIcons();

        // 1. 뷰 전환 제어
        function switchView(viewId) {{
            document.getElementById('view-landing').classList.add('hidden');
            document.getElementById('view-dashboard').classList.add('hidden');
            document.getElementById('view-custom-mac').classList.add('hidden');
            document.getElementById('canvas-sticky-wrap').classList.add('hidden');

            document.getElementById('nav-landing').className = "px-4 py-1.5 rounded-lg text-sm font-medium text-slate-400 hover:text-white transition-all";
            document.getElementById('nav-dashboard').className = "px-4 py-1.5 rounded-lg text-sm font-medium text-slate-400 hover:text-white transition-all";
            document.getElementById('nav-custom-mac').className = "px-4 py-1.5 rounded-lg text-sm font-medium text-slate-400 hover:text-white flex items-center gap-1.5 transition-all";

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
                if(btn) btn.className = "dash-tab-btn px-4 py-2 text-sm font-medium text-slate-500 hover:text-slate-900 border-b-2 border-transparent";
            }});

            const targetContent = document.getElementById('content-' + tabId);
            const targetBtn = document.getElementById('btntab-' + tabId);
            if(targetContent) targetContent.classList.remove('hidden');
            if(targetBtn) targetBtn.className = "dash-tab-btn px-4 py-2 text-sm font-bold border-b-2 border-blue-600 text-blue-600";

            if(tabId === 'tab-summary') {{
                setTimeout(() => {{ initOrUpdateCharts(); }}, 50);
            }}
        }}

        // 2. [Orakl 스타일 3D 스크롤리텔링 엔진]
        let globeScene, globeCamera, globeRenderer, globeGroup, organicSphere, dotParticles;
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

        // 실제 대륙 육지 여부 판정기
        function isLandArea(lat, lon) {{
            if (lat >= 10 && lat <= 70 && lon >= 60 && lon <= 145) {{
                if (lat < 25 && lon < 95 && lon > 70) return true;
                if (lat >= 20 && lon >= 95) return true;
                if (lat >= 40 && lon >= 60) return true;
            }}
            if (lat >= 35 && lat <= 70 && lon >= -10 && lon <= 45) return true;
            if (lat >= 15 && lat <= 72 && lon >= -168 && lon <= -55) {{
                if (lat < 30 && lon < -115) return false;
                return true;
            }}
            if (lat >= -55 && lat <= 12 && lon >= -82 && lon <= -34) return true;
            if (lat >= -35 && lat <= 36 && lon >= -18 && lon <= 52) return true;
            if (lat >= -44 && lat <= -10 && lon >= 112 && lon <= 154) return true;
            return false;
        }}

        function init3DGlobe() {{
            const container = document.getElementById('globe-container');
            if(!container) return;

            globeScene = new THREE.Scene();
            globeCamera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
            globeCamera.position.set(0, 0, 160);

            globeRenderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            globeRenderer.setSize(window.innerWidth, window.innerHeight);
            globeRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            container.appendChild(globeRenderer.domElement);

            globeGroup = new THREE.Group();
            globeScene.add(globeGroup);

            // A. 내부에서 유기적으로 '꾸물꾸물' 움직이는 노이즈 와이어프레임 코어 (Orakl 핵심 연출)
            const organicGeo = new THREE.IcosahedronGeometry(baseRadius * 0.9, 4);
            const organicMat = new THREE.MeshBasicMaterial({{
                color: 0x1d4ed8,
                wireframe: true,
                transparent: true,
                opacity: 0.35
            }});
            organicSphere = new THREE.Mesh(organicGeo, organicMat);
            globeGroup.add(organicSphere);

            // B. 실제 세계 대륙 도트 매트릭스 (외부 껍질)
            const dotPositions = [];
            const step = 3.0;
            for (let lat = -70; lat <= 75; lat += step) {{
                const latCos = Math.cos(lat * Math.PI / 180);
                const lonStep = step / Math.max(0.2, latCos);
                for (let lon = -180; lon < 180; lon += lonStep) {{
                    if (isLandArea(lat, lon)) {{
                        const pos = latLonToVec3(lat, lon, baseRadius);
                        dotPositions.push(pos.x, pos.y, pos.z);
                    }}
                }}
            }}

            const dotGeometry = new THREE.BufferGeometry();
            dotGeometry.setAttribute('position', new THREE.Float32BufferAttribute(dotPositions, 3));
            const dotMaterial = new THREE.PointsMaterial({{
                size: 2.2,
                color: 0x38bdf8,
                transparent: true,
                opacity: 0.95
            }});
            dotParticles = new THREE.Points(dotGeometry, dotMaterial);
            globeGroup.add(dotParticles);

            // C. 반도체 수출 대권항로 아크 (서울 기점)
            const hubs = [
                {{ lat: 37.56, lon: 126.97 }},
                {{ lat: 37.77, lon: -122.41 }},
                {{ lat: 24.78, lon: 120.99 }},
                {{ lat: 20.84, lon: 106.68 }},
                {{ lat: 51.05, lon: 13.73 }}
            ];

            function addTradeArc(from, to) {{
                const p1 = latLonToVec3(from.lat, from.lon, baseRadius + 0.5);
                const p2 = latLonToVec3(to.lat, to.lon, baseRadius + 0.5);
                const mid = p1.clone().add(p2).multiplyScalar(0.5);
                const dist = p1.distanceTo(p2);
                mid.setLength(baseRadius + dist * 0.25);

                const curve = new THREE.QuadraticBezierCurve3(p1, mid, p2);
                const pts = curve.getPoints(32);
                const geo = new THREE.BufferGeometry().setFromPoints(pts);
                const mat = new THREE.LineBasicMaterial({{ color: 0x00f0ff, transparent: true, opacity: 0.7 }});
                globeGroup.add(new THREE.Line(geo, mat));
            }}
            addTradeArc(hubs[0], hubs[1]);
            addTradeArc(hubs[0], hubs[2]);
            addTradeArc(hubs[0], hubs[3]);
            addTradeArc(hubs[0], hubs[4]);

            // D. 스크롤 위치 감지 (Scroll Progress 0.0 ~ 1.0)
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

            // 렌더 루프: 내부 파동('꾸물꾸물') + 스크롤 시 위치/스케일 보간(Lerp)
            function animate() {{
                requestAnimationFrame(animate);
                const time = clock.getElapsedTime();

                // 1. 내부 구체의 꼭짓점을 sin/cos으로 유기적으로 왜곡하여 '꾸물꾸물' 살아 숨쉬는 유체 효과 연출
                const posAttr = organicSphere.geometry.attributes.position;
                for (let i = 0; i < posAttr.count; i++) {{
                    const u = posAttr.getX(i);
                    const v = posAttr.getY(i);
                    const w = posAttr.getZ(i);
                    // 유기적 노이즈 파동
                    const wave = 1.0 + 0.035 * Math.sin(time * 2.5 + u * 0.05 + v * 0.05);
                    posAttr.setXYZ(i, u * wave, v * wave, w * wave);
                }}
                organicSphere.geometry.attributes.position.needsUpdate = true;

                // 2. 전체 지구 자전 회전
                globeGroup.rotation.y = time * 0.18;

                // 3. Orakl 스타일 스크롤리텔링:
                // 스크롤이 내려감에 따라 구체가 [중앙] -> [오른쪽 뒤로 이동하며 입체적 스케일 변화]
                const targetX = scrollYProgress * 38; 
                const targetY = -scrollYProgress * 8;
                const targetZ = scrollYProgress * 25; 
                const targetScale = 1.0 + scrollYProgress * 0.35;

                globeGroup.position.x += (targetX - globeGroup.position.x) * 0.08;
                globeGroup.position.y += (targetY - globeGroup.position.y) * 0.08;
                globeGroup.position.z += (targetZ - globeGroup.position.z) * 0.08;
                globeGroup.scale.set(targetScale, targetScale, targetScale);

                globeRenderer.render(globeScene, globeCamera);
            }}
            animate();
        }}
        init3DGlobe();

        // 3. 챗봇 엔진
        function toggleChatbot() {{
            const win = document.getElementById('chatbot-window');
            win.classList.toggle('hidden');
            if(!win.classList.contains('hidden')) {{
                document.getElementById('chat-input').focus();
            }}
        }}

        function appendMessage(text, isUser = false) {{
            const msgBox = document.getElementById('chat-messages');
            const wrap = document.createElement('div');
            wrap.className = isUser ? "flex justify-end" : "flex items-start gap-2";

            if(isUser) {{
                wrap.innerHTML = `<div class="chat-bubble-user p-3 max-w-[80%] leading-relaxed text-xs">${{text}}</div>`;
            }} else {{
                wrap.innerHTML = `
                    <div class="w-7 h-7 rounded-full bg-blue-100 overflow-hidden shrink-0 mt-0.5">
                        <img src="{chatbot_b64}" alt="AI" class="w-full h-full object-cover" onerror="this.src='https://api.dicebear.com/7.x/bottts/svg?seed=Axport';" />
                    </div>
                    <div class="chat-bubble-ai p-3 max-w-[80%] leading-relaxed text-xs">${{text}}</div>
                `;
            }}
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
                let ans = "해당 품목에 대한 추가 기술 제원을 입력해주시면 정밀하게 요건을 시뮬레이션해 드립니다.";
                if(q.includes("3A090") || q.includes("통제선") || q.includes("규제")) {{
                    ans = "<b>미 상무부 ECCN 3A090 규제 핵심 안내:</b><br>• <b>3A090.a</b>: TPP 4800 이상 고성능 가속기 칩은 사전 라이선스 의무화<br>• <b>3A090.b</b>: 연산밀도 충족 칩 사전 통보(NAC) 대상<br>• 웨이퍼 미세공정 <b>7nm 이하</b> 해당 시 시스템 자동 -15점 감점";
                }} else if(q.includes("RVC") || q.includes("원산지") || q.includes("부가가치") || q.includes("계산")) {{
                    ans = "<b>RVC(역내부가가치비율) 산출 공식:</b><br><code class='text-blue-600 bg-white px-1 rounded'>RVC = [(FOB - 비원산지재료비) / FOB] × 100</code><br>• 일반적인 반도체 FTA 기준은 <b>55.0% 이상</b>입니다.<br>• 미달 시 -20점 감점 처리됩니다.";
                }} else if(q.includes("HBM") || q.includes("미국") || q.includes("대미")) {{
                    ans = "<b>HBM3e 대미/글로벌 수출 가이드:</b><br>1. 최종 사용자 서약서(End-User Statement) 필수 확보<br>2. 동남아 우회 패키징 시 재수출 규제(FDPR) 점검<br>3. 데이터 진단 탭에서 실시간 적합도를 확인하세요.";
                }}
                appendMessage(ans, false);
            }}, 600);
        }}

        // 4. macOS 윈도우 드래그
        let highestZ = 30;
        function setupWindows() {{
            document.querySelectorAll('.mac-window').forEach(win => {{
                const header = win.querySelector('.window-drag-header');
                let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

                win.addEventListener('mousedown', () => {{
                    highestZ++;
                    win.style.zIndex = highestZ;
                }});

                if(header) {{
                    header.onmousedown = function(e) {{
                        e.preventDefault();
                        highestZ++;
                        win.style.zIndex = highestZ;
                        pos3 = e.clientX;
                        pos4 = e.clientY;
                        document.onmouseup = () => {{ document.onmouseup = null; document.onmousemove = null; }};
                        document.onmousemove = (ev) => {{
                            ev.preventDefault();
                            pos1 = pos3 - ev.clientX;
                            pos2 = pos4 - ev.clientY;
                            pos3 = ev.clientX;
                            pos4 = ev.clientY;
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
            const btn = document.getElementById(winId.replace('mac-', 'btn-'));
            if(win.style.display === 'none') {{
                win.style.display = 'block';
                if(btn) btn.classList.add('bg-blue-600');
            }} else {{
                win.style.display = 'none';
                if(btn) btn.classList.remove('bg-blue-600');
            }}
        }}

        // 5. Chart.js 안전 렌더링
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
                        borderColor: '#2563eb',
                        backgroundColor: 'rgba(37, 99, 235, 0.1)',
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
                        backgroundColor: ['#2563eb', '#38bdf8', '#818cf8', '#cbd5e1']
                    }}]
                }},
                options: {{ responsive: true, maintainAspectRatio: false }}
            }});
        }}

        // 6. 통화 스위칭
        let currentCurrency = 'USD';
        const EX_RATE = 1350;
        function setCurrency(curr) {{
            currentCurrency = curr;
            document.getElementById('curr-usd').className = curr === 'USD' ? "px-2.5 py-1 rounded-md bg-blue-600 text-white shadow-xs" : "px-2.5 py-1 rounded-md text-slate-400 hover:text-white";
            document.getElementById('curr-krw').className = curr === 'KRW' ? "px-2.5 py-1 rounded-md bg-blue-600 text-white shadow-xs" : "px-2.5 py-1 rounded-md text-slate-400 hover:text-white";

            document.querySelectorAll('.kpi-val').forEach(el => {{
                const usd = parseFloat(el.getAttribute('data-usd'));
                const unit = el.getAttribute('data-unit');
                if(curr === 'USD') {{
                    el.innerText = `$${{usd.toFixed(1)}}${{unit}}`;
                }} else {{
                    const krwTrillion = (usd * EX_RATE) / 10000;
                    el.innerText = `₩${{krwTrillion.toFixed(1)}}조`;
                }}
            }});
        }}

        // 7. 샘플 CSV 다운로드
        function downloadSampleCSV() {{
            const csvContent = "HS_CODE,PRODUCT_NAME,PROCESS_NODE_NM,TARGET_COUNTRY,UNIT_PRICE_USD,RVC_PERCENT,ECCN_FLAG\\n" +
                               "8542.31.1000,AI 가속기 HBM3e,4,미국,2850.0,68.5,3A090\\n" +
                               "8542.32.0000,서버용 DDR5 DRAM,12,대만,145.0,62.0,None\\n" +
                               "8542.39.0000,전력반도체 SiC 모듈,45,베트남,45.0,58.0,None\\n" +
                               "8542.31.9000,차량용 제어 MCU,28,독일,85.0,71.2,None";
            const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "axport_semiconductor_sample.csv";
            a.click();
            URL.revokeObjectURL(url);
        }}

        // 8. 초기 테이블 렌더링 & 파일 업로드
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
                    reasons.push("미 상무부 3A090 규제군 및 미세공정(≤7nm) 해당 (-15점)");
                }}
                if(r.rvc < 55.0) {{
                    score -= 20;
                    reasons.push("FTA 부가가치비율(RVC) 55% 미달 (-20점)");
                }}

                const badgeColor = score >= 80 ? "bg-emerald-100 text-emerald-800" : "bg-amber-100 text-amber-800";
                const reasonText = reasons.length ? reasons.join(" / ") : "만점 통과 (특이 규제 없음)";

                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td class="p-3 font-mono font-medium">${{r.hs}}</td>
                    <td class="p-3 font-bold text-slate-900">${{r.name}}</td>
                    <td class="p-3">${{r.node}} nm</td>
                    <td class="p-3">${{r.country}}</td>
                    <td class="p-3">$${{Number(r.price).toLocaleString()}}</td>
                    <td class="p-3">${{r.rvc}}%</td>
                    <td class="p-3"><span class="px-2.5 py-1 rounded-full text-xs font-bold ${{badgeColor}}">${{score}}점</span></td>
                    <td class="p-3 text-slate-500">${{reasonText}}</td>
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