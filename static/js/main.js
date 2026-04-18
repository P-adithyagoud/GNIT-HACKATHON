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
        
        // Confidence Badge
        const badge = document.getElementById('confidenceBadge');
        const text = document.getElementById('confidenceText');
        text.textContent = data.confidence || 'Medium';
        
        badge.className = 'status-badge'; // Reset
        const levelClass = (data.confidence || 'medium').toLowerCase();
        badge.classList.add(`confidence-${levelClass}`);

        // Summary & Root Cause
        document.getElementById('incidentSummary').textContent = data.incident_summary;
        document.getElementById('rootCauseText').textContent = data.root_cause;

        // Populate Lists
        this.populateList('resolutionList', data.resolution_steps, 'text-slate-300');
        this.populateList('immediateList', data.immediate_actions, 'text-amber-200');

        // Similar Incidents
        const similarSection = document.getElementById('similarIncidentsSection');
        const similarList = document.getElementById('similarIncidentsList');
        
        if (data.similar_incidents && data.similar_incidents.length > 0) {
            similarSection.classList.remove('hidden');
            similarList.innerHTML = data.similar_incidents.map(inc => `
                <div class="p-4 bg-slate-800/50 border border-white/5 rounded-xl">
                    <div class="text-xs font-bold text-blue-400 uppercase tracking-widest mb-2">Past Incident</div>
                    <div class="text-sm font-semibold text-white mb-2">${this.escape(inc.issue)}</div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-3 pt-3 border-t border-white/5">
                        <div>
                            <div class="text-[10px] uppercase text-slate-500 font-bold mb-1">Root Cause</div>
                            <div class="text-xs text-slate-400">${this.escape(inc.root_cause)}</div>
                        </div>
                        <div>
                            <div class="text-[10px] uppercase text-slate-500 font-bold mb-1">Resolution</div>
                            <div class="text-xs text-slate-400">${this.escape(inc.resolution)}</div>
                        </div>
                    </div>
                </div>
            `).join('');
        } else {
            similarSection.classList.add('hidden');
        }

        // Fallback Note
        this.fallbackIndicator.classList.toggle('hidden', !isFallback);
    }

    populateList(elementId, items, textClass) {
        const element = document.getElementById(elementId);
        element.innerHTML = items
            .map(item => `<li class="${textClass} text-sm leading-relaxed">${this.escape(item)}</li>`)
            .join('');
    }

    escape(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    handleCopy() {
        if (!this.resultData) return;

        const report = this.generateReport(this.resultData);
        navigator.clipboard.writeText(report).then(() => {
            const originalText = this.copyBtn.textContent;
            this.copyBtn.textContent = 'Copied to Clipboard!';
            this.copyBtn.classList.add('bg-green-600');
            
            setTimeout(() => {
                this.copyBtn.textContent = originalText;
                this.copyBtn.classList.remove('bg-green-600');
            }, 2000);
        });
    }

    generateReport(data) {
        return [
            'INCIDENT ANALYSIS REPORT',
            '========================',
            `Summary: ${data.incident_summary}`,
            `Confidence: ${data.confidence}`,
            '',
            'ROOT CAUSE:',
            `• ${data.root_cause}`,
            '',
            'RESOLUTION STEPS:',
            ...data.resolution_steps.map((s, i) => `${i + 1}. ${s}`),
            '',
            'IMMEDIATE ACTIONS:',
            ...data.immediate_actions.map(a => `• ${a}`)
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
