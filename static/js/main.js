/**
 * Main UI Controller
 * Handles DOM interactions, events, and UI state management.
 */

const EXAMPLE_INCIDENT = `API latency spike after deployment

Last 30 minutes:
- API response times: 200ms → 2500ms
- Error rate: 0.1% → 5%
- High CPU usage on pod cluster (82%)
- Memory usage stable

Recent deployment (15 min ago):
- Upgraded middleware from v2.1 to v3.0
- New connection pooling mechanism

Observations:
- Affects all API endpoints
- Correlates with deployment timing
- No external dependency issues

Current state: Under investigation, traffic partially rerouted`;

class UIController {
    constructor() {
        this.cacheElements();
        this.bindEvents();
        this.resultData = null;
    }

    cacheElements() {
        this.incidentInput = document.getElementById('incident');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        this.exampleBtn = document.getElementById('exampleBtn');
        this.copyBtn = document.getElementById('copyBtn');
        this.retryBtn = document.getElementById('retryBtn');
        this.loadingState = document.getElementById('loading');
        this.resultsSection = document.getElementById('results');
        this.errorSection = document.getElementById('error');
        this.charCounter = document.getElementById('charCount');
        this.fallbackIndicator = document.getElementById('fallbackNote');
    }

    bindEvents() {
        this.analyzeBtn.addEventListener('click', () => this.handleAnalyze());
        this.exampleBtn.addEventListener('click', () => this.handleLoadExample());
        this.copyBtn.addEventListener('click', () => this.handleCopy());
        this.retryBtn.addEventListener('click', () => this.handleReset());
        
        this.incidentInput.addEventListener('input', () => this.updateCharCount());
        this.incidentInput.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                this.handleAnalyze();
            }
        });
    }

    updateCharCount() {
        const count = this.incidentInput.value.length;
        this.charCounter.textContent = Math.min(count, 3000);
        
        if (count > 3000) {
            this.incidentInput.value = this.incidentInput.value.substring(0, 3000);
        }
    }

    handleLoadExample() {
        this.incidentInput.value = EXAMPLE_INCIDENT;
        this.updateCharCount();
        this.incidentInput.focus();
        // Visual feedback
        this.exampleBtn.classList.add('scale-95');
        setTimeout(() => {
            this.exampleBtn.classList.remove('scale-95');
            this.handleAnalyze();
        }, 150);
    }

    async handleAnalyze() {
        const text = this.incidentInput.value.trim();

        if (!text) {
            this.showErrorMessage('Please provide an incident logs or description.');
            return;
        }

        this.setUIProcessing(true);

        try {
            const result = await IncidentAPI.analyze(text);
            this.renderResults(result.data, result.fallback);
            this.setUIProcessing(false, true);
        } catch (error) {
            this.showErrorMessage(error.message);
            this.setUIProcessing(false, false);
        }
    }

    setUIProcessing(isProcessing, hasResults = false) {
        this.analyzeBtn.disabled = isProcessing;
        this.errorSection.classList.add('hidden');
        
        if (isProcessing) {
            this.resultsSection.classList.add('hidden');
            this.loadingState.classList.remove('hidden');
        } else {
            this.loadingState.classList.add('hidden');
            if (hasResults) {
                this.resultsSection.classList.remove('hidden');
                this.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    }

    renderResults(data, isFallback = false) {
        this.resultData = data;
        
        // Meta Badges (SEV, Complexity, Mode, Confidence)
        const complexityColors = {
            'easy': 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
            'medium': 'bg-amber-500/20 text-amber-400 border-amber-500/30',
            'hard': 'bg-orange-500/20 text-orange-400 border-orange-500/30'
        };
        const compClass = complexityColors[(data.complexity || 'medium').toLowerCase()] || complexityColors['medium'];

        const badgeContainer = document.getElementById('meta-badges');
        badgeContainer.innerHTML = `
            <span class="px-3 py-1 bg-red-500/20 text-red-400 text-xs font-bold rounded-lg border border-red-500/30 uppercase tracking-widest">${data.severity || 'SEV2'}</span>
            <span class="px-3 py-1 ${compClass} text-xs font-bold rounded-lg border uppercase tracking-widest">${data.complexity || 'MEDIUM'} FIX</span>
            <span class="px-3 py-1 bg-purple-500/20 text-purple-400 text-xs font-bold rounded-lg border border-purple-500/30 uppercase tracking-widest">MODE: ${data.mode || 'NEW'}</span>
            <span class="px-3 py-1 bg-blue-500/20 text-blue-400 text-xs font-bold rounded-lg border border-blue-500/30 uppercase tracking-widest">${data.confidence || 'Medium'} CONFIDENCE</span>
        `;

        // Text Content
        document.getElementById('incident-summary').textContent = data.summary || data.incident_summary;
        document.getElementById('root-cause').textContent = data.root_cause;

        // Populate Immediate Actions (Complex Objects)
        const immediateList = document.getElementById('immediate-actions');
        immediateList.innerHTML = (data.immediate_actions || []).map(action => `
            <li class="p-4 bg-white/5 rounded-lg border border-white/10 flex flex-col gap-2">
                <div class="flex items-center justify-between">
                    <span class="text-xs font-bold uppercase py-0.5 px-2 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30">${action.priority} priority</span>
                    <span class="text-[10px] items-center gap-1 font-bold uppercase px-2 py-0.5 rounded bg-blue-500/10 text-blue-300 border border-blue-500/20">
                        <i class="fas fa-user-shield"></i> ${action.owner}
                    </span>
                </div>
                <p class="text-white text-sm font-medium">${this.escape(action.step)}</p>
            </li>
        `).join('');

        // Populate Simple Lists
        this.populateSimpleList('resolution-steps', data.resolution_steps);
        this.populateSimpleList('validation-steps', data.validation_steps);
        this.populateSimpleList('preventive-measures', data.preventive_measures);

        // Similar Incidents (KEDB)
        const similarContainer = document.getElementById('similar-incidents-container');
        const similarList = document.getElementById('similar-incidents');
        
        if (data.similar_incidents && data.similar_incidents.length > 0) {
            similarContainer.classList.remove('hidden');
            similarList.innerHTML = data.similar_incidents.map(inc => `
                <div class="correlation-card group relative p-4 bg-white/5 border ${inc.is_primary_match ? 'border-blue-500/50 ring-1 ring-blue-500/30' : 'border-white/10'} rounded-xl cursor-pointer hover:bg-white/10 transition-all duration-300" onclick="this.classList.toggle('active')">
                    ${inc.is_primary_match ? `
                        <div class="absolute -top-3 -right-3 bg-blue-600 text-white text-[9px] font-bold px-2 py-1 rounded-full shadow-lg flex items-center gap-1">
                            <i class="fas fa-link"></i> PRIMARY
                        </div>
                    ` : ''}
                    
                    <div class="flex items-center justify-between mb-2">
                        <div class="text-[10px] font-bold ${inc.source === 'LOCAL KEDB' ? 'text-blue-400' : 'text-purple-400'} uppercase tracking-widest flex items-center gap-2">
                            <i class="fas ${inc.source === 'LOCAL KEDB' ? 'fa-database' : 'fa-cloud'}"></i> ${inc.source || 'KEDB'}
                        </div>
                        <i class="fas fa-chevron-down text-[10px] text-slate-500 chevron"></i>
                    </div>

                    <div class="text-sm font-bold text-white mb-1 truncate" title="${this.escape(inc.issue)}">${this.escape(inc.issue)}</div>
                    <div class="text-[10px] text-slate-400 line-clamp-1 group-[.active]:hidden">${this.escape(inc.resolution)}</div>

                    <div class="detail-expand space-y-3 pt-3 border-t border-white/5">
                        <div class="space-y-1">
                            <div class="text-[8px] font-bold text-blue-400 uppercase tracking-tighter">Historical Root Cause</div>
                            <div class="text-[11px] text-slate-300 leading-snug">${this.escape(inc.root_cause)}</div>
                        </div>
                        <div class="space-y-1">
                            <div class="text-[8px] font-bold text-emerald-400 uppercase tracking-tighter">Standard Resolution</div>
                            <div class="text-[11px] text-slate-300 leading-snug">${this.escape(inc.resolution)}</div>
                        </div>
                    </div>
                </div>
            `).join('');
        } else {
            similarContainer.classList.add('hidden');
        }

        // Fallback Note
        this.fallbackIndicator.classList.toggle('hidden', !isFallback);
    }

    populateSimpleList(elementId, items) {
        const element = document.getElementById(elementId);
        if (!element) return;
        element.innerHTML = (items || [])
            .map(item => `<li class="text-gray-300 text-sm py-1">${this.escape(item)}</li>`)
            .join('');
    }

    escape(str) {
        if (!str) return '';
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    handleCopy() {
        if (!this.resultData) return;

        const report = this.generateReport(this.resultData);
        navigator.clipboard.writeText(report).then(() => {
            const originalText = this.copyBtn.textContent;
            this.copyBtn.innerHTML = '<i class="fas fa-check"></i> Analysis Copied!';
            this.copyBtn.classList.remove('bg-blue-600');
            this.copyBtn.classList.add('bg-emerald-600');
            
            setTimeout(() => {
                this.copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy Full Analysis';
                this.copyBtn.classList.remove('bg-emerald-600');
                this.copyBtn.classList.add('bg-blue-600');
            }, 2000);
        });
    }

    generateReport(data) {
        return [
            `SRE INCIDENT COMMANDER REPORT [${data.severity || 'SEV2'}]`,
            '==========================================',
            `Summary: ${data.summary || data.incident_summary}`,
            `Mode: ${data.mode || 'NEW'} | Confidence: ${data.confidence}`,
            '',
            'ROOT CAUSE ANALYSIS:',
            `• ${data.root_cause}`,
            '',
            'IMMEDIATE ACTIONS (PRIORITY):',
            ...(data.immediate_actions || []).map(a => `• [${a.priority.toUpperCase()}] ${a.owner}: ${a.step}`),
            '',
            'PERMANENT RESOLUTION:',
            ...(data.resolution_steps || []).map((s, i) => `${i + 1}. ${s}`),
            '',
            'SYSTEM VALIDATION:',
            ...(data.validation_steps || []).map(v => `• ${v}`),
            '',
            'PREVENTIVE MEASURES:',
            ...(data.preventive_measures || []).map(p => `• ${p}`)
        ].join('\n');
    }

    showErrorMessage(msg) {
        document.getElementById('errorText').textContent = msg;
        this.errorSection.classList.remove('hidden');
    }

    handleReset() {
        this.incidentInput.value = '';
        this.updateCharCount();
        this.resultsSection.classList.add('hidden');
        this.errorSection.classList.add('hidden');
        this.incidentInput.focus();
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    window.app = new UIController();
});
