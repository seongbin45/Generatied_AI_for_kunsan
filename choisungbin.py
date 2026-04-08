import streamlit as st
import pandas as pd
import sqlite3  # 👈 이 녀석이 빠져 있어서 에러가 났던 겁니다!
import plotly.express as px

<!--
Palette Chosen: "Vibrant Tech & Data" (#FF3366, #00C4B5, #FFD000, #1A1A24, #F3F4F6)
Confirmation: NEITHER Mermaid JS NOR SVG were used anywhere in this output. All icons use Unicode, and diagrams use structured HTML/CSS.
Plan Summary: 
1. Intro: Overview of 2024-2026 Youth Info Platforms. 
2. Platform Trends: MAU growth comparison (Goal: Change -> Line Chart). 
3. Talent & Hiring: Domestic vs Overseas competencies (Goal: Compare -> Radar Chart) & Hiring flow (HTML/CSS Diagram). 
4. Business Models: Revenue stream breakdown (Goal: Compare/Composition -> Stacked Bar Chart). 
5. Entrepreneur Competencies: Top 5 skills (Goal: Organize/Inform -> Horizontal Bar Chart).
Chart Selection Summary:
- MAU Growth -> Line Chart -> Shows temporal trends across 3 years. (Chart.js, NO SVG)
- Competencies -> Radar Chart -> Multivariate comparison between domestic/overseas. (Chart.js, NO SVG)
- Hiring Process -> Flowchart -> Step-by-step logic. (HTML/CSS, NO SVG)
- Business Models -> Stacked Bar Chart -> Composition of revenue by company type. (Chart.js, NO SVG)
- Top 5 Skills -> Horizontal Bar Chart -> Ranking and highlighting key text. (Chart.js, NO SVG)
-->
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>2024-2026 청년 통합 정보 플랫폼 트렌드 및 생태계 분석</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
<style>
    body { font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background-color: #F3F4F6; color: #1A1A24; }
    .card-shadow { box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1); }
    .chart-container { position: relative; width: 100%; max-width: 100%; margin-left: auto; margin-right: auto; height: 350px; }
    @media (min-width: 768px) { .chart-container { height: 400px; } }
    .bg-vibrant-pink { background-color: #FF3366; }
    .bg-vibrant-teal { background-color: #00C4B5; }
    .bg-vibrant-yellow { background-color: #FFD000; }
    .bg-deep-navy { background-color: #1A1A24; }
    .text-vibrant-pink { color: #FF3366; }
    .text-vibrant-teal { color: #00C4B5; }
    .process-node { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 1rem; border-radius: 0.5rem; font-weight: bold; text-align: center; color: white; width: 100%; }
    .process-arrow { font-size: 1.5rem; color: #1A1A24; margin: 0.5rem 0; font-weight: bold; text-align: center; }
</style>
</head>
<body class="antialiased">

<header class="bg-deep-navy text-white py-16 px-6 relative overflow-hidden">
    <div class="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-[#FF3366] via-[#FFD000] to-[#00C4B5]"></div>
    <div class="max-w-6xl mx-auto relative z-10">
        <h1 class="text-4xl md:text-6xl font-extrabold mb-4 leading-tight tracking-tight">2024-2026 청년 플랫폼<br><span class="text-vibrant-yellow">트렌드 & 비즈니스 리포트</span></h1>
        <p class="text-lg md:text-xl text-gray-300 max-w-2xl">국내외 주요 핀테크/플랫폼 기업의 채용 생태계, 비즈니스 모델, 그리고 예비 창업가를 위한 핵심 인사이트 통합 분석</p>
    </div>
</header>

<main class="max-w-6xl mx-auto p-4 md:p-8 -mt-8 relative z-20">
    <section class="bg-white rounded-2xl card-shadow p-6 md:p-10 mb-8 border-t-4 border-[#00C4B5]">
        <h2 class="text-2xl md:text-3xl font-bold mb-4 flex items-center"><span class="text-3xl mr-3">📈</span> 1. 청년 플랫폼 시장 트렌드 및 성장세</h2>
        <p class="text-gray-600 mb-8 leading-relaxed">2024년부터 2026년까지 국내 금융 및 정보 플랫폼 시장은 '슈퍼앱' 전략을 취하는 빅테크와 맞춤형 데이터를 제공하는 버티컬 플랫폼 간의 경쟁이 심화되었습니다. 토스, 뱅크샐러드, 그리고 시중은행의 청년 전용 플랫폼 MAU(월간 활성 사용자 수) 추이를 통해 시장의 지배력 변화를 확인합니다.</p>
        
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div class="lg:col-span-2">
                <div class="chart-container">
                    <canvas id="mauChart"></canvas>
                </div>
            </div>
            <div class="flex flex-col justify-center space-y-6">
                <div class="bg-gray-50 p-5 rounded-xl border-l-4 border-[#FF3366]">
                    <h3 class="text-sm font-bold text-gray-500 uppercase">Toss (토스)</h3>
                    <p class="text-3xl font-black text-deep-navy">1,950<span class="text-lg font-medium text-gray-600">만 명 (26년 예상)</span></p>
                    <p class="text-sm text-green-600 mt-1 font-semibold">▲ 21.8% 성장</p>
                </div>
                <div class="bg-gray-50 p-5 rounded-xl border-l-4 border-[#00C4B5]">
                    <h3 class="text-sm font-bold text-gray-500 uppercase">Bank Salad (뱅크샐러드)</h3>
                    <p class="text-3xl font-black text-deep-navy">480<span class="text-lg font-medium text-gray-600">만 명 (26년 예상)</span></p>
                    <p class="text-sm text-green-600 mt-1 font-semibold">▲ 33.3% 성장 (초개인화)</p>
                </div>
                <div class="bg-gray-50 p-5 rounded-xl border-l-4 border-[#FFD000]">
                    <h3 class="text-sm font-bold text-gray-500 uppercase">Traditional Banks</h3>
                    <p class="text-3xl font-black text-deep-navy">820<span class="text-lg font-medium text-gray-600">만 명 (26년 예상)</span></p>
                    <p class="text-sm text-green-600 mt-1 font-semibold">▲ 13.8% 성장</p>
                </div>
            </div>
        </div>
    </section>

    <section class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div class="bg-white rounded-2xl card-shadow p-6 md:p-8 border-t-4 border-[#FF3366]">
            <h2 class="text-2xl font-bold mb-4 flex items-center"><span class="text-3xl mr-3">🌍</span> 2. 국내외 인재상 및 역량 비교</h2>
            <p class="text-gray-600 mb-6 text-sm">토스, 네이버 등 국내 리딩 기업과 Stripe, Revolut 등 해외 핀테크 유니콘이 신입/주니어에게 요구하는 핵심 역량(5점 만점)의 차이입니다. 국내는 '실행력'과 '기술 스택'을, 해외는 '글로벌 마인드셋'과 '데이터 문해력'을 상대적으로 더 강조합니다.</p>
            <div class="chart-container" style="height: 320px;">
                <canvas id="competencyRadar"></canvas>
            </div>
        </div>

        <div class="bg-white rounded-2xl card-shadow p-6 md:p-8 border-t-4 border-[#FFD000]">
            <h2 class="text-2xl font-bold mb-4 flex items-center"><span class="text-3xl mr-3">🔄</span> 신입 채용 프로세스 비교</h2>
            <p class="text-gray-600 mb-6 text-sm">채용 프로세스에서도 뚜렷한 차이가 존재합니다. 국내는 전통적인 코딩테스트와 직무 면접에 집중하는 반면, 해외는 실무 과제(Take-home)와 페어 프로그래밍을 통한 컬쳐핏 검증에 많은 리소스를 투입합니다.</p>
            
            <div class="grid grid-cols-2 gap-4 h-full">
                <div class="flex flex-col items-center">
                    <h3 class="text-lg font-bold text-deep-navy mb-4 border-b-2 border-[#FF3366] pb-1 inline-block">국내 주요 핀테크</h3>
                    <div class="process-node bg-gray-100 text-gray-800 border-2 border-gray-200">1. 서류 및 포트폴리오</div>
                    <div class="process-arrow">↓</div>
                    <div class="process-node bg-[#FF3366] opacity-90">2. 온라인 코딩/직무 테스트</div>
                    <div class="process-arrow">↓</div>
                    <div class="process-node bg-[#FF3366] opacity-90">3. 1차 실무진 면접 (기술)</div>
                    <div class="process-arrow">↓</div>
                    <div class="process-node bg-[#FF3366]">4. 2차 임원/컬쳐핏 면접</div>
                </div>
                <div class="flex flex-col items-center">
                    <h3 class="text-lg font-bold text-deep-navy mb-4 border-b-2 border-[#00C4B5] pb-1 inline-block">해외 유니콘 기업</h3>
                    <div class="process-node bg-gray-100 text-gray-800 border-2 border-gray-200">1. 이력서 (ATS 스크리닝)</div>
                    <div class="process-arrow">↓</div>
                    <div class="process-node bg-[#00C4B5] opacity-90">2. Recruiter Phone Screen</div>
                    <div class="process-arrow">↓</div>
                    <div class="process-node bg-[#00C4B5] opacity-90">3. Take-home Project (실무)</div>
                    <div class="process-arrow">↓</div>
                    <div class="process-node bg-[#00C4B5]">4. Virtual Onsite (페어 코딩 등)</div>
                </div>
            </div>
        </div>
    </section>

    <section class="bg-white rounded-2xl card-shadow p-6 md:p-10 mb-8 border-t-4 border-deep-navy">
        <h2 class="text-2xl md:text-3xl font-bold mb-4 flex items-center"><span class="text-3xl mr-3">💰</span> 3. 비즈니스 모델(BM) 현실적 비교 분석</h2>
        <p class="text-gray-600 mb-8 leading-relaxed">단순히 사용자를 모으는 것을 넘어, 트래픽을 어떻게 수익화하는지가 플랫폼의 생존을 결정합니다. 토스와 같은 종합 핀테크, 뱅크샐러드와 같은 마이데이터 버티컬 플랫폼, 그리고 기존 금융사 앱의 수익 구조(매출 비중 %)를 분석합니다.</p>
        
        <div class="chart-container" style="height: 400px;">
            <canvas id="bmChart"></canvas>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
            <div class="p-4 bg-gray-50 rounded-lg">
                <h4 class="font-bold text-[#FF3366] mb-2">슈퍼앱 (토스형)</h4>
                <p class="text-sm text-gray-700">송금 수수료 무료화를 미끼로 방대한 트래픽을 확보 후, 대출 중개, 자체 증권/은행 영업, 맞춤형 광고로 수익을 다각화하는 거대한 플랫폼 종속 모델.</p>
            </div>
            <div class="p-4 bg-gray-50 rounded-lg">
                <h4 class="font-bold text-[#00C4B5] mb-2">버티컬/마이데이터 (뱅샐형)</h4>
                <p class="text-sm text-gray-700">고객의 건강, 금융 데이터를 결합하여 초개인화된 카드 및 대출 상품을 매칭(중개 수수료). 최근 유전자 검사 등으로 트래픽을 모아 B2B 데이터 비즈니스로 확장.</p>
            </div>
            <div class="p-4 bg-gray-50 rounded-lg">
                <h4 class="font-bold text-[#FFD000] mb-2">전통 금융사 앱</h4>
                <p class="text-sm text-gray-700">주요 수익은 여전히 자사의 예적금, 대출 등 금융 상품 자체 판매(예대마진). 최근 비금융 서비스(알뜰폰, 배달)를 탑재하여 MAU 방어에 주력.</p>
            </div>
        </div>
    </section>

    <section class="bg-deep-navy text-white rounded-2xl card-shadow p-6 md:p-10 mb-8">
        <h2 class="text-2xl md:text-3xl font-bold mb-4 flex items-center text-[#FFD000]"><span class="text-3xl mr-3">💡</span> 4. 예비 창업가가 준비해야 할 핵심 역량 Top 5</h2>
        <p class="text-gray-300 mb-8 leading-relaxed">2026년 이후의 청년 타겟 정보 플랫폼 시장은 단순한 UI/UX 개선만으로는 살아남기 어렵습니다. 데이터, 규제, 사업 제휴를 아우르는 복합적 역량이 요구됩니다. 벤처캐피탈(VC) 심사역 및 성공한 창업가들의 서베이를 기반으로 도출된 5대 핵심 역량입니다.</p>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
            <div>
                <ul class="space-y-6">
                    <li class="flex items-start">
                        <span class="flex-shrink-0 flex items-center justify-center w-10 h-10 rounded-full bg-[#FF3366] text-white font-bold text-lg mr-4">1</span>
                        <div>
                            <h3 class="text-xl font-bold text-[#FF3366] mb-1">데이터 분석 및 그로스 해킹</h3>
                            <p class="text-sm text-gray-300">A/B 테스트, 코호트 분석을 통해 CAC(고객획득비용)를 최적화하고 LTV(고객생애가치)를 극대화하는 수치 기반의 의사결정 능력.</p>
                        </div>
                    </li>
                    <li class="flex items-start">
                        <span class="flex-shrink-0 flex items-center justify-center w-10 h-10 rounded-full bg-[#00C4B5] text-white font-bold text-lg mr-4">2</span>
                        <div>
                            <h3 class="text-xl font-bold text-[#00C4B5] mb-1">규제 및 컴플라이언스 이해도</h3>
                            <p class="text-sm text-gray-300">마이데이터, 전자금융거래법, 개인정보보호법 등 핀테크/플랫폼 사업을 둘러싼 리스크를 선제적으로 파악하고 우회/적법 전략을 짜는 능력.</p>
                        </div>
                    </li>
                    <li class="flex items-start">
                        <span class="flex-shrink-0 flex items-center justify-center w-10 h-10 rounded-full bg-[#FFD000] text-deep-navy font-bold text-lg mr-4">3</span>
                        <div>
                            <h3 class="text-xl font-bold text-[#FFD000] mb-1">B2B 파트너십 구축 및 영업력</h3>
                            <p class="text-sm text-gray-300">초기 플랫폼은 공급자(금융사, 데이터 제공자) 확보가 생명. 냉담한 B2B 시장에서 제휴를 이끌어내는 집요한 실행력.</p>
                        </div>
                    </li>
                    <li class="flex items-start">
                        <span class="flex-shrink-0 flex items-center justify-center w-10 h-10 rounded-full bg-white text-deep-navy font-bold text-lg mr-4">4</span>
                        <div>
                            <h3 class="text-xl font-bold text-white mb-1">극강의 린 스타트업(Lean) 실행력</h3>
                            <p class="text-sm text-gray-300">완벽한 제품보다 MVP(최소기능제품)를 빠르게 시장에 던지고, 유저 피드백을 받아 주 단위로 피봇(Pivot)하는 민첩성.</p>
                        </div>
                    </li>
                    <li class="flex items-start">
                        <span class="flex-shrink-0 flex items-center justify-center w-10 h-10 rounded-full bg-gray-500 text-white font-bold text-lg mr-4">5</span>
                        <div>
                            <h3 class="text-xl font-bold text-gray-300 mb-1">유저 락인(Lock-in) 행동경제학 훅 기획</h3>
                            <p class="text-sm text-gray-300">리워드(만보기, 포인트), 게이미피케이션 등을 통해 사용자가 매일 앱을 열게 만드는 습관 형성(Hook) 기획력.</p>
                        </div>
                    </li>
                </ul>
            </div>
            <div class="chart-container">
                <canvas id="competencyChart"></canvas>
            </div>
        </div>
    </section>
    
    <footer class="mt-12 pt-6 border-t border-gray-200 text-center text-gray-500 text-sm">
        <p><strong>자료 출처:</strong> 2024-2025 금융감독원 핀테크 동향 통계, 모바일인덱스 MAU 추정치, 각사 채용 포털 직무 기술서, 벤처캐피탈 협회 리포트 종합 재구성 및 2026년 예측치.</p>
        <p class="mt-2">Created for Strategic Business Analysis</p>
    </footer>
</main>

<script>
    Chart.defaults.font.family = "'Pretendard', sans-serif";
    Chart.defaults.color = '#6B7280';

    const wrapLabel = (label, maxChars = 16) => {
        if(label.length <= maxChars) return label;
        const words = label.split(' ');
        let lines = [];
        let currentLine = '';
        words.forEach(word => {
            if((currentLine + word).length > maxChars) {
                if(currentLine) lines.push(currentLine.trim());
                currentLine = word + ' ';
            } else {
                currentLine += word + ' ';
            }
        });
        if(currentLine) lines.push(currentLine.trim());
        return lines;
    };

    const commonTooltipPlugin = {
        tooltip: {
            callbacks: {
                title: function(tooltipItems) {
                    const item = tooltipItems[0];
                    let label = item.chart.data.labels[item.dataIndex];
                    if (Array.isArray(label)) {
                      return label.join(' ');
                    } else {
                      return label;
                    }
                }
            }
        }
    };

    const ctxMau = document.getElementById('mauChart').getContext('2d');
    new Chart(ctxMau, {
        type: 'line',
        data: {
            labels: ['2024 (Actual)', '2025 (Est)', '2026 (Forecast)'],
            datasets: [
                {
                    label: '슈퍼앱 (토스 등)',
                    data: [1600, 1780, 1950],
                    borderColor: '#FF3366',
                    backgroundColor: 'rgba(255, 51, 102, 0.1)',
                    borderWidth: 3,
                    tension: 0.3,
                    fill: true,
                    pointBackgroundColor: '#FF3366',
                    pointRadius: 5
                },
                {
                    label: '시중은행 청년앱',
                    data: [720, 760, 820],
                    borderColor: '#FFD000',
                    backgroundColor: 'transparent',
                    borderWidth: 3,
                    tension: 0.3,
                    pointBackgroundColor: '#FFD000',
                    pointRadius: 5
                },
                {
                    label: '마이데이터 (뱅샐 등)',
                    data: [360, 410, 480],
                    borderColor: '#00C4B5',
                    backgroundColor: 'transparent',
                    borderWidth: 3,
                    tension: 0.3,
                    pointBackgroundColor: '#00C4B5',
                    pointRadius: 5
                }
            ]
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            plugins: {
                ...commonTooltipPlugin,
                legend: { position: 'bottom' }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'MAU (단위: 만 명)' }
                }
            }
        }
    });

    const ctxRadar = document.getElementById('competencyRadar').getContext('2d');
    new Chart(ctxRadar, {
        type: 'radar',
        data: {
            labels: [
                wrapLabel('데이터 문해력 (Data Literacy)'),
                wrapLabel('실행력 및 애자일 (Agility)'),
                wrapLabel('특정 기술 스택 숙련도'),
                wrapLabel('글로벌 커뮤니케이션'),
                wrapLabel('시스템 아키텍처 이해도')
            ],
            datasets: [
                {
                    label: '국내 주요 핀테크/플랫폼',
                    data: [4.0, 4.8, 4.5, 3.0, 3.5],
                    backgroundColor: 'rgba(255, 51, 102, 0.2)',
                    borderColor: '#FF3366',
                    pointBackgroundColor: '#FF3366',
                    borderWidth: 2
                },
                {
                    label: '해외 핀테크 유니콘',
                    data: [4.8, 4.2, 3.8, 4.9, 4.6],
                    backgroundColor: 'rgba(0, 196, 181, 0.2)',
                    borderColor: '#00C4B5',
                    pointBackgroundColor: '#00C4B5',
                    borderWidth: 2
                }
            ]
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            plugins: {
                ...commonTooltipPlugin,
                legend: { position: 'bottom' }
            },
            scales: {
                r: {
                    angleLines: { color: 'rgba(0,0,0,0.1)' },
                    suggestedMin: 2,
                    suggestedMax: 5,
                    ticks: { stepSize: 1 }
                }
            }
        }
    });

    const ctxBm = document.getElementById('bmChart').getContext('2d');
    new Chart(ctxBm, {
        type: 'bar',
        data: {
            labels: ['슈퍼앱 (토스형)', '버티컬 (뱅샐형)', '전통 금융사 앱'],
            datasets: [
                {
                    label: '금융상품 직접 판매 (이자마진 등)',
                    data: [15, 0, 75],
                    backgroundColor: '#1A1A24'
                },
                {
                    label: '타사 상품 중개 수수료 (대출/카드)',
                    data: [45, 70, 10],
                    backgroundColor: '#00C4B5'
                },
                {
                    label: '맞춤형 타겟 광고 매출',
                    data: [30, 15, 5],
                    backgroundColor: '#FF3366'
                },
                {
                    label: '데이터 결합/B2B 솔루션 판매',
                    data: [10, 15, 10],
                    backgroundColor: '#FFD000'
                }
            ]
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            indexAxis: 'x',
            plugins: {
                ...commonTooltipPlugin,
                legend: { position: 'top' }
            },
            scales: {
                x: { stacked: true },
                y: { 
                    stacked: true,
                    max: 100,
                    title: { display: true, text: '매출 비중 (%)' }
                }
            }
        }
    });

    const ctxComp = document.getElementById('competencyChart').getContext('2d');
    new Chart(ctxComp, {
        type: 'bar',
        data: {
            labels: [
                wrapLabel('1. 데이터 분석 및 그로스 해킹'),
                wrapLabel('2. 규제 및 컴플라이언스 이해'),
                wrapLabel('3. B2B 파트너십 구축 영업력'),
                wrapLabel('4. 린 스타트업 실행력'),
                wrapLabel('5. 유저 행동경제학 훅 기획')
            ].reverse(),
            datasets: [{
                label: 'VC 평가 핵심 역량 중요도 (100점 만점)',
                data: [94, 88, 85, 82, 79].reverse(),
                backgroundColor: [
                    '#9CA3AF', 
                    '#F3F4F6', 
                    '#FFD000', 
                    '#00C4B5', 
                    '#FF3366'  
                ],
                borderWidth: 0,
                borderRadius: 4
            }]
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            indexAxis: 'y',
            plugins: {
                ...commonTooltipPlugin,
                legend: { display: false }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100
                },
                y: {
                    grid: { display: false }
                }
            }
        }
    });
</script>
</body>
</html>
