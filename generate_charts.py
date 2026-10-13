import matplotlib.pyplot as plt

# Set up the figure with two subplots side-by-side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Apply IEEE academic style styling
plt.style.use('bmh')

# --- Subplot 1: Latency Bar Chart ---
layers = ['Layer 1\n(Vector Shield)', 'Layer 2\n(Cognitive LLM)']
latencies = [20, 550]  # Average latencies in ms based on report
errors = [5, 250]      # Variance (15-25ms and 300-800ms)

bars = ax1.bar(layers, latencies, yerr=errors, capsize=8, color=['#4a6fa5', '#c65911'], edgecolor='black', alpha=0.9)
ax1.set_ylabel('Inference Latency (ms)')
ax1.set_title('Average Defense Latency per Layer', fontweight='bold')
ax1.set_yscale('log') # Log scale because difference is massive
ax1.set_ylim(bottom=1) # Set bottom limit for log scale

# Add text labels on top of bars
for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval * 1.5, f'~{yval}ms', ha='center', va='bottom', fontweight='bold')


# --- Subplot 2: Mitigation Distribution Pie Chart ---
labels = ['Blocked by Layer 1\n(Known Semantic Threats)', 'Analyzed by Layer 2\n(Novel / Zero-Day)']
sizes = [95.2, 4.8] # 95% of attacks are blocked early
colors = ['#548235', '#fce4d6']
explode = (0.05, 0)  

ax2.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=120, wedgeprops={'edgecolor': 'black', 'linewidth': 1})
ax2.set_title('Threat Mitigation Distribution', fontweight='bold')

plt.tight_layout()
output_path = r'C:\Users\moham\OneDrive\Documents\my-qdrant-project\screenshots\performance_metrics.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Success! Saved academic chart to {output_path}")
