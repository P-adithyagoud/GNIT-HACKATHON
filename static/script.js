const EXAMPLE_INCIDENT = "API latency spike after deployment\n\nLast 30 minutes:\n- API response times: 200ms → 2500ms\n- Error rate: 0.1% → 5%\n- High CPU usage on pod cluster (82%)\n- Memory usage stable\n\nRecent deployment (15 min ago):\n- Upgraded middleware from v2.1 to v3.0\n- New connection pooling mechanism\n\nObservations:\n- Affects all API endpoints\n- Correlates with deployment timing\n- No external dependency issues\n\nCurrent state: Under investigation, traffic partially rerouted";

class IncidentAnalyzer {
    constructor() {
        this.setupElements();
        this.setupEventListeners();
    }

    setupElements() {
        this.incident = document.getElementById('incident');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        this.exampleBtn = document.getElementById('exampleBtn');
        this.copyBtn = document.getElementById('copyBtn');
        this.retryBtn = document.getElementById('retryBtn');
        this.loading = document.getElementById('loading');
        this.results = document.getElementById('results');
        this.error = document.getElementById('error');
        this.charCount = document.getElementById('charCount');
        this.fallbackNote = document.getElementById('fallbackNote');
    }

    setupEventListeners() {
        this.analyzeBtn.addEventListener('click', () => this.analyze());
        this.exampleBtn.addEventListener('click', () => this.loadExample());
        this.copyBtn.addEventListener('click', () => this.copyResults());
        this.retryBtn.addEventListener('click', () => this.reset());
        this.incident.addEventListener('input', () => this.updateCharCount());
        this.incident.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                this.analyze();
            }
        });
    }

    updateCharCount() {
        const count = this.incident.value.length;
        this.charCount.textContent = Math.min(count, 3000);
        
        if (count > 3000) {
            this.incident.value = this.incident.value.substring(0, 3000);
        }
    }

    loadExample() {
        this.incident.value = EXAMPLE_INCIDENT;
        this.updateCharCount();
        this.incident.focus();
        setTimeout(() => this.analyze(), 100);
    }

    async analyze() {
        const text = this.incident.value.trim();

        if (!text) {
            this.showError('Please enter an incident description');
            return;
        }

        this.analyzeBtn.disabled = true;
        this.error.classList.add('hidden');
        this.results.classList.add('hidden');
        this.loading.classList.remove('hidden');

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ incident: text })
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || 'Analysis failed');
            }

            this.displayResults(data.data, data.fallback);
            this.loading.classList.add('hidden');
            this.results.classList.remove('hidden');
            this.results.scrollIntoView({ behavior: 'smooth', block: 'start' });

        } catch (error) {
            this.showError(`Error: ${error.message}`);
            this.loading.classList.add('hidden');
        } finally {
            this.analyzeBtn.disabled = false;
        }
    }

    displayResults(data, isFallback = false) {
        this.setConfidenceBadge(data.confidence);
        this.displayList('rootCausesList', data.root_causes, 'red');
        this.displayList('resolutionList', data.resolution_steps, 'blue');
        this.displayList('immediateList', data.priority_actions.immediate, 'amber');
        this.displayList('shortTermList', data.priority_actions.short_term, 'slate');
        this.displayList('longTermList', data.priority_actions.long_term, 'slate');

        if (isFallback) {
            this.fallbackNote.classList.remove('hidden');
        } else {
            this.fallbackNote.classList.add('hidden');
        }

        this.currentResult = data;
    }

    setConfidenceBadge(level) {
        const badge = document.getElementById('confidenceBadge');
        const text = document.getElementById('confidenceText');

        text.textContent = level;

        badge.classList.remove('confidence-high', 'confidence-medium', 'confidence-low');

        if (level === 'High') {
            badge.classList.add('confidence-high');
        } else if (level === 'Medium') {
            badge.classList.add('confidence-medium');
        } else {
            badge.classList.add('confidence-low');
        }
    }

    displayList(elementId, items, color) {
        const element = document.getElementById(elementId);
        const colorMap = {
            red: 'text-red-400',
            blue: 'text-blue-400',
            amber: 'text-amber-200',
            slate: 'text-slate-300'
        };

        element.innerHTML = items
            .map(item => `<li class="${colorMap[color] || 'text-slate-300'} text-sm leading-relaxed">${this.escapeHtml(item)}</li>`)
            .join('');
    }

    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    copyResults() {
        if (!this.currentResult) return;

        const text = this.formatResultsAsText(this.currentResult);
        navigator.clipboard.writeText(text).then(() => {
            const btn = this.copyBtn;
            const originalText = btn.textContent;
            btn.textContent = 'Copied!';
            setTimeout(() => {
                btn.textContent = originalText;
            }, 2000);
        });
    }

    formatResultsAsText(data) {
        const lines = [
            'INCIDENT ANALYSIS REPORT',
            '========================',
            '',
            `Confidence: ${data.confidence}`,
            '',
            'ROOT CAUSES:',
            ...data.root_causes.map(cause => `• ${cause}`),
            '',
            'RESOLUTION STEPS:',
            ...data.resolution_steps.map((step, i) => `${i + 1}. ${step}`),
            '',
            'PRIORITY ACTIONS:',
            '',
            'Immediate Mitigation:',
            ...data.priority_actions.immediate.map(action => `• ${action}`),
            '',
            'Short-term Recovery:',
            ...data.priority_actions.short_term.map(action => `• ${action}`),
            '',
            'Long-term Hardening:',
            ...data.priority_actions.long_term.map(action => `• ${action}`)
        ];

        return lines.join('\n');
    }

    showError(message) {
        document.getElementById('errorText').textContent = message;
        this.error.classList.remove('hidden');
        this.error.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    reset() {
        this.incident.value = '';
        this.updateCharCount();
        this.results.classList.add('hidden');
        this.error.classList.add('hidden');
        this.incident.focus();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new IncidentAnalyzer();
});
