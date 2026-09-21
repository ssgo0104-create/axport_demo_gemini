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

# 3. 완성형 단일 소스
raw_html = """
<!DOCTYPE html>
<html lang="ko">
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
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Inter:wght@400;500;600;700;800&display=swap');
        * { font-family: 'Inter', -apple-system, sans-serif; }
        
        .logo-font {
            font-family: 'Montserrat', sans-serif;
            font-weight: 900;
        }

        .mac-glass {
            background: rgba(255, 255, 255, 0.94);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            box-shadow: 0 20px 45px -12px rgba(0, 0, 0, 0.35);
        }
        .mac-desktop-bg {
            background: radial-gradient(circle at 50% 20%, #1e3a8a 0%, #0f172a 60%, #020617 100%);
        }

        /* 윈도우 실제 크기 조절(Resizable) */
        .mac-window {
            position: absolute;
            resize: both;
            overflow: auto;
            min-width: 280px;
            min-height: 180px;
            max-width: 90vw;
            max-height: 85vh;
        }
        .window-drag-header { 
            cursor: grab; 
            user-select: none; 
        }
        .window-drag-header:active { 
            cursor: grabbing; 
        }

        .kpi-gradient-blue { background: linear-gradient(135deg, #2563eb, #1d4ed8); }
        .kpi-gradient-green { background: linear-gradient(135deg, #10b981, #059669); }
        .kpi-gradient-purple { background: linear-gradient(135deg, #8b5cf6, #7c3aed); }
        .kpi-gradient-amber { background: linear-gradient(135deg, #f59e0b, #d97706); }
        
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
    </style>
</head>
<body class="bg-[#F8FAFC] text-slate-800 antialiased overflow-x-hidden min-h-screen">

    <!-- 글로벌 헤더 -->
    <header class="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center gap-6">
                <!-- Axport 정밀 원본 일치 로고 (SVG) -->
                <div class="cursor-pointer flex items-center select-none" onclick="switchView('landing')">
                    <svg width="155" height="48" viewBox="0 0 200 65" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <!-- 'A' 심볼 (네이비 #0E2344) -->
                        <polygon points="36,4 12,46 25,46 31,35 48,35 42,23 39,23 43,14" fill="#0E2344"/>
                        <polygon points="33,31 46,31 39,18" fill="#FFFFFF"/>
                        <!-- 'X' 심볼의 회색 대각선 기둥 (\) -->
                        <polygon points="41,17 52,32 38,46 49,46 59,34 50,21" fill="#9CA3AF"/>
                        <!-- 'X' 심볼의 네이비 상승 화살표 기둥 (/) -->
                        <polygon points="46,46 64,22 71,28 56,46" fill="#0E2344"/>
                        <polygon points="61,8 77,20 63,22" fill="#0E2344"/>
                        <!-- 하단 볼드 타이포그래피 AXPORT -->
                        <text x="8" y="60" class="logo-font" font-size="16" fill="#0E2344" letter-spacing="3.5">AXPORT</text>
                    </svg>
                </div>

                <!-- 뷰 전환 탭 -->
                <nav class="hidden md:flex items-center gap-1 bg-slate-100 p-1 rounded-xl">
                    <button onclick="switchView('landing')" id="nav-landing" class="px-4 py-1.5 rounded-lg text-sm font-semibold transition-all bg-white text-blue-600 shadow-sm">회사 소개 (홈)</button>
                    <button onclick="switchView('dashboard')" id="nav-dashboard" class="px-4 py-1.5 rounded-lg text-sm font-medium text-slate-600 hover:text-slate-900 transition-all">메인 대시보드</button>
                    <button onclick="switchView('custom-mac')" id="nav-custom-mac" class="px-4 py-1.5 rounded-lg text-sm font-medium text-slate-600 hover:text-slate-900 flex items-center gap-1.5 transition-all">
                        <i data-lucide="layout-grid" class="w-4 h-4"></i> 사용자 커스텀 뷰
                    </button>
                </nav>
            </div>

            <!-- 우측 환율 토글 & 평가기준 버튼 -->
            <div class="flex items-center gap-3">
                <button onclick="openEvaluationModal()" class="flex items-center gap-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-bold px-3 py-1.5 rounded-lg border border-indigo-200 transition-all">
                    <i data-lucide="help-circle" class="w-4 h-4 text-indigo-600"></i> 평가 기준표 안내
                </button>
                <div class="flex items-center bg-slate-100 rounded-lg p-1 text-xs font-semibold">
                    <button id="curr-usd" onclick="setCurrency('USD')" class="px-2.5 py-1 rounded-md bg-white text-blue-600 shadow-xs">USD ($)</button>
                    <button id="curr-krw" onclick="setCurrency('KRW')" class="px-2.5 py-1 rounded-md text-slate-500 hover:text-slate-800">KRW (₩)</button>
                </div>
            </div>
        </div>
    </header>

    <!-- ================= VIEW 1: 회사 소개 & 정밀 3D 대륙 와이어프레임 지구본 ================= -->
    <section id="view-landing" class="block">
        <div class="relative w-full h-[88vh] bg-[#070F1E] overflow-hidden flex items-center">
            <!-- 3D 지구본 캔버스 -->
            <div id="globe-container" class="absolute inset-0 z-0"></div>
            
            <div class="relative z-10 max-w-7xl mx-auto px-6 sm:px-8 w-full pointer-events-none">
                <div class="max-w-2xl text-white space-y-6">
                    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/20 border border-blue-400/30 text-blue-300 text-xs font-semibold backdrop-blur-md">
                        <span class="w-2 h-2 rounded-full bg-blue-400 animate-ping"></span>
                        Semiconductor Export Compliance AI Platform
                    </div>
                    <h1 class="text-4xl sm:text-6xl font-extrabold tracking-tight leading-tight text-white drop-shadow-md">
                        반도체 수출 적합성의 <br><span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">새로운 기준, Axport</span>
                    </h1>
                    <p class="text-slate-300 text-base sm:text-lg leading-relaxed pointer-events-auto">
                        미 상무부 수출통제(ECCN 3A090), 원산지 부가가치기준(RVC)을 기업 데이터 원본 그대로 자동 정제하고 진단합니다.
                    </p>
                    <div class="flex flex-wrap gap-4 pt-2 pointer-events-auto">
                        <button onclick="switchView('dashboard')" class="bg-blue-600 hover:bg-blue-500 text-white font-bold px-6 py-3.5 rounded-xl shadow-lg shadow-blue-600/30 transition-all flex items-center gap-2 text-sm">
                            <i data-lucide="gauge" class="w-4 h-4"></i> 메인 대시보드 바로가기
                        </button>
                        <button onclick="switchView('custom-mac')" class="bg-slate-800/90 hover:bg-slate-700/90 text-slate-200 border border-slate-700 font-semibold px-5 py-3.5 rounded-xl backdrop-blur-md transition-all flex items-center gap-2 text-sm">
                            <i data-lucide="layout" class="w-4 h-4"></i> 사용자 커스텀 뷰 열기
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 3대 핵심 강점 안내 -->
        <div class="max-w-7xl mx-auto px-6 py-20">
            <div class="text-center max-w-3xl mx-auto mb-16">
                <h2 class="text-xs font-bold uppercase tracking-wider text-blue-600 mb-2">Platform Strength</h2>
                <h3 class="text-3xl font-extrabold text-slate-900">수출 기업 맞춤형 원스톱 인텔리전스</h3>
            </div>
            <div class="grid md:grid-cols-3 gap-8">
                <div class="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
                    <div class="w-12 h-12 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center mb-6">
                        <i data-lucide="database" class="w-6 h-6"></i>
                    </div>
                    <h4 class="text-xl font-bold text-slate-900 mb-3">1. Zero-ETL 자동 정제</h4>
                    <p class="text-slate-600 text-sm leading-relaxed">자체 포맷의 인보이스/ERP 데이터를 넣기만 해도 통화 환산과 결측치를 자동 보정하여 업무 공수를 획기적으로 줄입니다.</p>
                </div>
                <div class="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
                    <div class="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-600 flex items-center justify-center mb-6">
                        <i data-lucide="shield-check" class="w-6 h-6"></i>
                    </div>
                    <h4 class="text-xl font-bold text-slate-900 mb-3">2. 투명한 감점 원인 규명</h4>
                    <p class="text-slate-600 text-sm leading-relaxed">왜 이런 점수가 나왔는지 규제 조항과 RVC 산출식을 투명하게 공개하고, 담당자가 직접 재검수할 수 있도록 지원합니다.</p>
                </div>
                <div class="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
                    <div class="w-12 h-12 rounded-xl bg-purple-100 text-purple-600 flex items-center justify-center mb-6">
                        <i data-lucide="activity" class="w-6 h-6"></i>
                    </div>
                    <h4 class="text-xl font-bold text-slate-900 mb-3">3. 실시간 매크로 모니터링</h4>
                    <p class="text-slate-600 text-sm leading-relaxed">DRAM 현물 가격 지수, 외환 변동성, 주요국 세관의 보류 리스크를 실시간 연동해 선제적 대응을 가능하게 합니다.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- ================= VIEW 2: 메인 기본 대시보드 ================= -->
    <section id="view-dashboard" class="hidden max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
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
                    <div class="h-64 relative">
                        <canvas id="chart-timeline"></canvas>
                    </div>
                </div>
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">
                    <div class="flex items-center justify-between mb-4">
                        <h4 class="font-bold text-slate-800 text-sm flex items-center gap-2">
                            <i data-lucide="pie-chart" class="w-4 h-4 text-blue-600"></i> 주요국 수출 점유율
                        </h4>
                    </div>
                    <div class="h-64 relative flex items-center justify-center">
                        <canvas id="chart-pie"></canvas>
                    </div>
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

                <div>
                    <h4 class="font-bold text-slate-800 text-sm mb-3">상세 판정 가이드 및 감점 규정</h4>
                    <table class="w-full text-xs text-left border-collapse border border-slate-200">
                        <thead class="bg-slate-50 text-slate-700 font-semibold">
                            <tr>
                                <th class="p-2.5 border border-slate-200">평가 항목</th>
                                <th class="p-2.5 border border-slate-200">정상 기준 (합격)</th>
                                <th class="p-2.5 border border-slate-200">감점 및 보완 조건</th>
                                <th class="p-2.5 border border-slate-200">적용 배점 조항</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-200 text-slate-600">
                            <tr>
                                <td class="p-2.5 border font-semibold">전략물자 통제 (ECCN)</td>
                                <td class="p-2.5 border text-emerald-700">EAR99 또는 범용 비통제 품목</td>
                                <td class="p-2.5 border text-red-600">3A090 첨단 칩 또는 7nm 이하 미세공정 (-15점)</td>
                                <td class="p-2.5 border">기술 규제 (35점 중)</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 border font-semibold">원산지 부가가치 (RVC)</td>
                                <td class="p-2.5 border text-emerald-700">RVC 55.0% 이상 확보</td>
                                <td class="p-2.5 border text-red-600">RVC 55% 미만 시 FTA 혜택 불가 판정 (-20점)</td>
                                <td class="p-2.5 border">원산지 기준 (30점 중)</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 border font-semibold">수출 대상국 통관 위험</td>
                                <td class="p-2.5 border text-emerald-700">세관 검사율 5% 미만 국가 (미국, 대만)</td>
                                <td class="p-2.5 border text-amber-600">정밀 검사율 10% 초과 국가 경유 시 서약서 요구 (-10점)</td>
                                <td class="p-2.5 border">통관 리스크 (20점 중)</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-600">
                    💡 <b>판정 기준 종합 합격선</b>: 총점 <b>80점 이상</b>인 경우 "수출 승인 적합 (PASS)", 80점 미만인 경우 추가 라이선스 발급 및 서류 보완이 필요한 "검토 요망 (REVIEW)"으로 자동 분류됩니다.
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
    </section>

    <!-- ================= VIEW 3: 사용자 커스텀 뷰 (실제 크기조절 Resizable 완벽 지원) ================= -->
    <section id="view-custom-mac" class="hidden relative w-full h-[88vh] mac-desktop-bg overflow-hidden">
        <div class="absolute top-4 left-1/2 -translate-x-1/2 z-50 flex items-center gap-2 bg-white/20 backdrop-blur-xl border border-white/30 px-4 py-2 rounded-2xl shadow-xl">
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
        <div id="mac-win1" class="mac-window w-80 mac-glass rounded-2xl shadow-2xl" style="top: 80px; left: 40px; z-index: 20;">
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
        <div id="mac-win2" class="mac-window w-96 mac-glass rounded-2xl shadow-2xl" style="top: 80px; left: 380px; z-index: 21;">
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
        <div id="mac-win3" class="mac-window w-84 mac-glass rounded-2xl shadow-2xl" style="top: 300px; left: 100px; z-index: 22;">
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
        <div id="mac-win4" class="mac-window w-80 mac-glass rounded-2xl shadow-2xl" style="top: 280px; left: 520px; z-index: 23;">
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

    <!-- 평가 기준 안내 모달 -->
    <div id="modal-eval" class="hidden fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
        <div class="bg-white max-w-2xl w-full rounded-2xl p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
            <div class="flex justify-between items-center border-b pb-3">
                <h3 class="font-bold text-slate-900 text-base">📋 Axport 반도체 수출 적합성 평가 공식 안내</h3>
                <button onclick="closeEvaluationModal()" class="text-slate-400 hover:text-slate-600">
                    <i data-lucide="x" class="w-5 h-5"></i>
                </button>
            </div>
            <div class="text-xs space-y-3 text-slate-600 leading-relaxed">
                <p>본 플랫폼은 100점 만점으로 반도체 수출 품목의 안전성을 점수화하며 세부 산출식은 다음과 같습니다:</p>
                <div class="p-3 bg-slate-100 rounded-xl font-mono text-[11px] text-slate-800">
                    최종 적합성 점수 = 100 - [ECCN 기술통제 감점] - [RVC 원산지 미달 감점] - [세관 보류 리스크 감점]
                </div>
                <ul class="list-disc pl-5 space-y-1.5">
                    <li><b>ECCN 3A090 통제선 (-15점)</b>: 웨이퍼 공정이 7nm 이하이거나 미 상무부 첨단 가속기 칩 규격에 부합할 경우 감점되며 수출 허가 서약서가 요구됩니다.</li>
                    <li><b>원산지 부가가치기준 미달 (-20점)</b>: RVC 비율이 FTA 기준치(55%) 미만일 경우 원산지 증명 혜택에서 제외됩니다.</li>
                    <li><b>세관 정밀 검사율 (-10점)</b>: 대상국의 최근 6개월 세관 검사율이 10% 이상인 경우 보완 서류를 요구합니다.</li>
                </ul>
            </div>
            <div class="text-right pt-2">
                <button onclick="closeEvaluationModal()" class="bg-blue-600 text-white font-bold text-xs px-4 py-2 rounded-xl">확인했습니다</button>
            </div>
        </div>
    </div>

    <!-- JS 스크립트: 완벽한 대륙 형태의 3D 글로브 엔진 탑재 -->
    <script>
        lucide.createIcons();

        // 1. 뷰 전환 제어
        function switchView(viewId) {
            document.getElementById('view-landing').classList.add('hidden');
            document.getElementById('view-dashboard').classList.add('hidden');
            document.getElementById('view-custom-mac').classList.add('hidden');

            document.getElementById('nav-landing').className = "px-4 py-1.5 rounded-lg text-sm font-medium text-slate-600 hover:text-slate-900 transition-all";
            document.getElementById('nav-dashboard').className = "px-4 py-1.5 rounded-lg text-sm font-medium text-slate-600 hover:text-slate-900 transition-all";
            document.getElementById('nav-custom-mac').className = "px-4 py-1.5 rounded-lg text-sm font-medium text-slate-600 hover:text-slate-900 flex items-center gap-1.5 transition-all";

            if(viewId === 'landing') {
                document.getElementById('view-landing').classList.remove('hidden');
                document.getElementById('nav-landing').className = "px-4 py-1.5 rounded-lg text-sm font-semibold transition-all bg-white text-blue-600 shadow-sm";
            } else if(viewId === 'dashboard') {
                document.getElementById('view-dashboard').classList.remove('hidden');
                document.getElementById('nav-dashboard').className = "px-4 py-1.5 rounded-lg text-sm font-semibold transition-all bg-white text-blue-600 shadow-sm";
                setTimeout(() => { initOrUpdateCharts(); }, 50);
            } else if(viewId === 'custom-mac') {
                document.getElementById('view-custom-mac').classList.remove('hidden');
                document.getElementById('nav-custom-mac').className = "px-4 py-1.5 rounded-lg text-sm font-semibold transition-all bg-white text-blue-600 shadow-sm flex items-center gap-1.5";
            }
        }

        function switchDashTab(tabId) {
            ['tab-summary', 'tab-upload', 'tab-criteria', 'tab-risks', 'tab-macro'].forEach(t => {
                const content = document.getElementById('content-' + t);
                const btn = document.getElementById('btntab-' + t);
                if(content) content.classList.add('hidden');
                if(btn) btn.className = "dash-tab-btn px-4 py-2 text-sm font-medium text-slate-500 hover:text-slate-900 border-b-2 border-transparent";
            });

            const targetContent = document.getElementById('content-' + tabId);
            const targetBtn = document.getElementById('btntab-' + tabId);
            if(targetContent) targetContent.classList.remove('hidden');
            if(targetBtn) targetBtn.className = "dash-tab-btn px-4 py-2 text-sm font-bold border-b-2 border-blue-600 text-blue-600";

            if(tabId === 'tab-summary') {
                setTimeout(() => { initOrUpdateCharts(); }, 50);
            }
        }

        function openEvaluationModal() { document.getElementById('modal-eval').classList.remove('hidden'); }
        function closeEvaluationModal() { document.getElementById('modal-eval').classList.add('hidden'); }

        // 2. [핵심] 실제 전 세계 대륙 경계선 데이터 기반 무결성 3D 지구본 엔진
        let globeScene, globeCamera, globeRenderer, globeGroup;
        let targetCameraZ = 190;

        function latLonToVec3(lat, lon, radius) {
            const phi = (90 - lat) * (Math.PI / 180);
            const theta = (lon + 180) * (Math.PI / 180);
            return new THREE.Vector3(
                -(radius * Math.sin(phi) * Math.cos(theta)),
                radius * Math.cos(phi),
                radius * Math.sin(phi) * Math.sin(theta)
            );
        }

        function init3DGlobe() {
            const container = document.getElementById('globe-container');
            if(!container) return;

            globeScene = new THREE.Scene();
            globeCamera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
            globeCamera.position.z = 190;

            globeRenderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            globeRenderer.setSize(container.clientWidth, container.clientHeight);
            globeRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            container.appendChild(globeRenderer.domElement);

            globeGroup = new THREE.Group();
            globeScene.add(globeGroup);

            const R = 64;

            // 베이스 딥 네이비 구체
            const baseSphere = new THREE.Mesh(
                new THREE.SphereGeometry(R - 0.4, 48, 48),
                new THREE.MeshBasicMaterial({ color: 0x07152b, transparent: true, opacity: 0.96 })
            );
            globeGroup.add(baseSphere);

            // 위도/경도 그리드
            const gridMat = new THREE.LineBasicMaterial({ color: 0x1e3a8a, transparent: true, opacity: 0.25 });
            for (let lat = -60; lat <= 60; lat += 30) {
                const ringPts = [];
                for (let lon = 0; lon <= 360; lon += 8) ringPts.push(latLonToVec3(lat, lon, R));
                globeGroup.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(ringPts), gridMat));
            }
            for (let lon = 0; lon < 360; lon += 45) {
                const meridPts = [];
                for (let lat = -85; lat <= 85; lat += 5) meridPts.push(latLonToVec3(lat, lon, R));
                globeGroup.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(meridPts), gridMat));
            }

            // 실제 대륙 해안선 세그먼트 (절대 깨지지 않는 유려한 라인)
            const continents = [
                // 동아시아 / 한국 / 일본
                [[37.5, 127], [35, 129], [34, 131], [35, 136], [38, 141], [43, 145], [45, 142], [40, 140], [35, 135], [33, 130]],
                [[38, 128], [42, 130], [40, 124], [37, 126], [35, 126], [35, 129]],
                // 유라시아 본토 (중국, 인도, 중동, 유럽)
                [[31, 122], [22, 114], [10, 107], [1, 104], [10, 99], [22, 91], [22, 70], [25, 62], [30, 48], [40, 53], [46, 48], [45, 36], [40, 26], [45, 13], [54, 8], [60, 5], [70, 28], [72, 68], [75, 110], [70, 160], [60, 170], [45, 142], [38, 120], [31, 122]],
                // 북아메리카
                [[15, -92], [20, -105], [30, -115], [34, -120], [48, -125], [58, -137], [65, -165], [70, -150], [72, -128], [68, -100], [60, -75], [50, -60], [40, -74], [30, -81], [25, -80], [22, -97], [16, -95], [15, -92]],
                // 남아메리카
                [[10, -75], [-5, -80], [-20, -70], [-40, -73], [-54, -68], [-45, -60], [-23, -43], [-5, -35], [5, -52], [10, -62], [10, -75]],
                // 아프리카
                [[35, -5], [32, 32], [12, 44], [-5, 40], [-25, 33], [-34, 18], [-15, 12], [5, 2], [15, -17], [28, -12], [35, -5]],
                // 호주 (오세아니아)
                [[-15, 130], [-22, 114], [-34, 115], [-37, 140], [-38, 146], [-28, 153], [-15, 145], [-12, 136], [-15, 130]]
            ];

            const coastLineMat = new THREE.LineBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.85, linewidth: 2 });
            continents.forEach(poly => {
                const pts = poly.map(([lat, lon]) => latLonToVec3(lat, lon, R + 0.3));
                pts.push(pts[0]);
                globeGroup.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), coastLineMat));
            });

            // 반도체 거점 허브 핀 & 발광 링
            const hubs = [
                { name: "서울", lat: 37.56, lon: 126.97 },
                { name: "실리콘밸리", lat: 37.77, lon: -122.41 },
                { name: "대만 신주", lat: 24.78, lon: 120.99 },
                { name: "베트남", lat: 21.02, lon: 105.83 },
                { name: "유럽", lat: 51.05, lon: 13.73 }
            ];

            hubs.forEach(h => {
                const pos = latLonToVec3(h.lat, h.lon, R + 0.6);
                const dot = new THREE.Mesh(
                    new THREE.SphereGeometry(1.6, 12, 12),
                    new THREE.MeshBasicMaterial({ color: 0x00f0ff })
                );
                dot.position.copy(pos);
                globeGroup.add(dot);

                const ring = new THREE.Mesh(
                    new THREE.RingGeometry(2.0, 2.8, 16),
                    new THREE.MeshBasicMaterial({ color: 0x00f0ff, side: THREE.DoubleSide, transparent: true, opacity: 0.7 })
                );
                ring.position.copy(pos);
                ring.lookAt(0, 0, 0);
                globeGroup.add(ring);
            });

            // 반도체 수출 대권항로 아크
            function addTradeArc(from, to) {
                const p1 = latLonToVec3(from.lat, from.lon, R + 0.6);
                const p2 = latLonToVec3(to.lat, to.lon, R + 0.6);
                const mid = p1.clone().add(p2).multiplyScalar(0.5);
                const dist = p1.distanceTo(p2);
                mid.setLength(R + dist * 0.26);

                const curve = new THREE.QuadraticBezierCurve3(p1, mid, p2);
                const pts = curve.getPoints(32);
                const geo = new THREE.BufferGeometry().setFromPoints(pts);
                const mat = new THREE.LineBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.75 });
                globeGroup.add(new THREE.Line(geo, mat));
            }

            addTradeArc(hubs[0], hubs[1]);
            addTradeArc(hubs[0], hubs[2]);
            addTradeArc(hubs[0], hubs[3]);
            addTradeArc(hubs[0], hubs[4]);

            // 마우스 휠 부드러운 줌인
            window.addEventListener('wheel', (e) => {
                if(document.getElementById('view-landing').classList.contains('hidden')) return;
                targetCameraZ = Math.max(110, Math.min(240, targetCameraZ + e.deltaY * 0.15));
            });

            function animate() {
                requestAnimationFrame(animate);
                globeGroup.rotation.y += 0.0024;
                globeCamera.position.z += (targetCameraZ - globeCamera.position.z) * 0.08;
                globeRenderer.render(globeScene, globeCamera);
            }
            animate();
        }
        init3DGlobe();

        // 3. macOS 창 드래그 & 리사이즈(실제 크기조절 작동)
        let highestZ = 30;
        function setupWindows() {
            document.querySelectorAll('.mac-window').forEach(win => {
                const header = win.querySelector('.window-drag-header');
                let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

                win.addEventListener('mousedown', () => {
                    highestZ++;
                    win.style.zIndex = highestZ;
                });

                if(header) {
                    header.onmousedown = function(e) {
                        e.preventDefault();
                        highestZ++;
                        win.style.zIndex = highestZ;
                        pos3 = e.clientX;
                        pos4 = e.clientY;
                        document.onmouseup = () => { document.onmouseup = null; document.onmousemove = null; };
                        document.onmousemove = (ev) => {
                            ev.preventDefault();
                            pos1 = pos3 - ev.clientX;
                            pos2 = pos4 - ev.clientY;
                            pos3 = ev.clientX;
                            pos4 = ev.clientY;
                            win.style.top = (win.offsetTop - pos2) + "px";
                            win.style.left = (win.offsetLeft - pos1) + "px";
                        };
                    };
                }
            });
        }
        setupWindows();

        function toggleMacWindow(winId) {
            const win = document.getElementById(winId);
            const btn = document.getElementById(winId.replace('mac-', 'btn-'));
            if(win.style.display === 'none') {
                win.style.display = 'block';
                if(btn) btn.classList.add('bg-blue-600');
            } else {
                win.style.display = 'none';
                if(btn) btn.classList.remove('bg-blue-600');
            }
        }

        // 4. Chart.js 안전 렌더링
        let chartTimeline = null;
        let chartPie = null;
        function initOrUpdateCharts() {
            const ctxTimeline = document.getElementById('chart-timeline');
            const ctxPie = document.getElementById('chart-pie');
            if(!ctxTimeline || !ctxPie) return;

            if(chartTimeline) chartTimeline.destroy();
            if(chartPie) chartPie.destroy();

            chartTimeline = new Chart(ctxTimeline, {
                type: 'line',
                data: {
                    labels: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월'],
                    datasets: [{
                        label: '수출액 ($B)',
                        data: [9.2, 9.8, 10.4, 10.1, 11.2, 11.8, 12.3, 12.5, 12.8],
                        borderColor: '#2563eb',
                        backgroundColor: 'rgba(37, 99, 235, 0.1)',
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });

            chartPie = new Chart(ctxPie, {
                type: 'doughnut',
                data: {
                    labels: ['아시아', '북미', '유럽', '기타'],
                    datasets: [{
                        data: [42, 28, 15, 15],
                        backgroundColor: ['#2563eb', '#38bdf8', '#818cf8', '#cbd5e1']
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
        }

        // 5. 통화 스위칭
        let currentCurrency = 'USD';
        const EX_RATE = 1350;
        function setCurrency(curr) {
            currentCurrency = curr;
            document.getElementById('curr-usd').className = curr === 'USD' ? "px-2.5 py-1 rounded-md bg-white text-blue-600 shadow-xs" : "px-2.5 py-1 rounded-md text-slate-500 hover:text-slate-800";
            document.getElementById('curr-krw').className = curr === 'KRW' ? "px-2.5 py-1 rounded-md bg-white text-blue-600 shadow-xs" : "px-2.5 py-1 rounded-md text-slate-500 hover:text-slate-800";

            document.querySelectorAll('.kpi-val').forEach(el => {
                const usd = parseFloat(el.getAttribute('data-usd'));
                const unit = el.getAttribute('data-unit');
                if(curr === 'USD') {
                    el.innerText = `$${usd.toFixed(1)}${unit}`;
                } else {
                    const krwTrillion = (usd * EX_RATE) / 10000;
                    el.innerText = `₩${krwTrillion.toFixed(1)}조`;
                }
            });
        }

        // 6. 샘플 CSV 다운로드
        function downloadSampleCSV() {
            const csvContent = "HS_CODE,PRODUCT_NAME,PROCESS_NODE_NM,TARGET_COUNTRY,UNIT_PRICE_USD,RVC_PERCENT,ECCN_FLAG\\n" +
                               "8542.31.1000,AI 가속기 HBM3e,4,미국,2850.0,68.5,3A090\\n" +
                               "8542.32.0000,서버용 DDR5 DRAM,12,대만,145.0,62.0,None\\n" +
                               "8542.39.0000,전력반도체 SiC 모듈,45,베트남,45.0,58.0,None\\n" +
                               "8542.31.9000,차량용 제어 MCU,28,독일,85.0,71.2,None";
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "axport_semiconductor_sample.csv";
            a.click();
            URL.revokeObjectURL(url);
        }

        // 7. 초기 테이블 렌더링 & 파일 업로드
        const initialDummyRows = [
            { hs: "8542.31.1000", name: "AI 가속기 HBM3e", node: 4, country: "미국", price: 2850, rvc: 68.5, eccn: "3A090" },
            { hs: "8542.32.0000", name: "서버용 DDR5 DRAM", node: 12, country: "대만", price: 145, rvc: 62.0, eccn: "None" },
            { hs: "8542.39.0000", name: "전력반도체 SiC 모듈", node: 45, country: "베트남", price: 45, rvc: 58.0, eccn: "None" }
        ];

        function renderTableRows(rows) {
            const tbody = document.getElementById('diagnosis-tbody');
            if(!tbody) return;
            tbody.innerHTML = '';
            rows.forEach(r => {
                let score = 100;
                let reasons = [];
                if(r.node <= 7 || r.eccn === "3A090") {
                    score -= 15;
                    reasons.push("미 상무부 3A090 규제군 및 미세공정(≤7nm) 해당 (-15점)");
                }
                if(r.rvc < 55.0) {
                    score -= 20;
                    reasons.push("FTA 부가가치비율(RVC) 55% 미달 (-20점)");
                }

                const badgeColor = score >= 80 ? "bg-emerald-100 text-emerald-800" : "bg-amber-100 text-amber-800";
                const reasonText = reasons.length ? reasons.join(" / ") : "만점 통과 (특이 규제 없음)";

                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td class="p-3 font-mono font-medium">${r.hs}</td>
                    <td class="p-3 font-bold text-slate-900">${r.name}</td>
                    <td class="p-3">${r.node} nm</td>
                    <td class="p-3">${r.country}</td>
                    <td class="p-3">$${Number(r.price).toLocaleString()}</td>
                    <td class="p-3">${r.rvc}%</td>
                    <td class="p-3"><span class="px-2.5 py-1 rounded-full text-xs font-bold ${badgeColor}">${score}점</span></td>
                    <td class="p-3 text-slate-500">${reasonText}</td>
                `;
                tbody.appendChild(tr);
            });
        }
        renderTableRows(initialDummyRows);

        function handleFileUpload(e) {
            const file = e.target.files[0];
            if(!file) return;
            const reader = new FileReader();
            reader.onload = function(evt) {
                const lines = evt.target.result.split('\\n').filter(l => l.trim().length > 0);
                const parsed = [];
                for(let i = 1; i < lines.length; i++) {
                    const cols = lines[i].split(',');
                    if(cols.length >= 6) {
                        parsed.push({
                            hs: cols[0].trim(),
                            name: cols[1].trim(),
                            node: parseInt(cols[2]) || 28,
                            country: cols[3].trim(),
                            price: parseFloat(cols[4]) || 100,
                            rvc: parseFloat(cols[5]) || 60,
                            eccn: cols[6] ? cols[6].trim() : "None"
                        });
                    }
                }
                if(parsed.length) {
                    renderTableRows(parsed);
                    alert("성공적으로 " + parsed.length + "건의 데이터를 분석했습니다.");
                }
            };
            reader.readAsText(file);
        }
    </script>
</body>
</html>
"""

# Streamlit 풀스크린 임베딩
components.html(raw_html, height=1000, scrolling=True)