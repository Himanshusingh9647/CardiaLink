# Add a function to calculate the insurance premium based on the composite score
def calculate_insurance_premium(risk_score):
    """
    Calculate insurance premium based on the following risk tiers:
    0-50%: Low - $320-$490
    51-65%: Medium - $580-$900
    66-85%: High - $950-$1,500
    86-100%: Critical - $1,600-$2,800
    
    Returns a tuple of (risk_tier, min_premium, max_premium)
    """
    risk_percentage = risk_score * 100
    
    if risk_percentage <= 50:
        return "Low", 320, 490
    elif risk_percentage <= 65:
        return "Medium", 580, 900
    elif risk_percentage <= 85:
        return "High", 950, 1500
    else:
        return "Critical", 1600, 2800

# After DIABETES_TEMPLATE, completely replace the existing RESULTS_TEMPLATE with this updated version
RESULTS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Combined Health Risk Assessment - CardiaLink Quantify</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --background: #ffffff;
            --foreground: #0f172a;
            --primary: #3b82f6;
            --primary-hover: #2563eb;
            --primary-foreground: #ffffff;
            --secondary: #f1f5f9;
            --secondary-foreground: #1e293b;
            --muted: #f1f5f9;
            --muted-foreground: #64748b;
            --border: #e2e8f0;
            --radius: 0.5rem;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', system-ui, sans-serif;
            background-color: #f8fafc;
            color: var(--foreground);
            line-height: 1.5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem;
        }
        
        .header {
            background-color: var(--background);
            border-bottom: 1px solid var(--border);
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
            position: sticky;
            top: 0;
            z-index: 50;
        }
        
        .header-inner {
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 4rem;
        }
        
        .logo {
            display: flex;
            align-items: center;
            font-weight: 600;
            font-size: 1.25rem;
            color: var(--foreground);
            text-decoration: none;
        }
        
        .logo svg {
            width: 1.5rem;
            height: 1.5rem;
            margin-right: 0.5rem;
        }
        
        .tabs {
            display: flex;
            gap: 1rem;
            padding: 0 1rem;
            border-bottom: 1px solid var(--border);
            background-color: var(--background);
        }
        
        .tab {
            padding: 0.75rem 1rem;
            border-bottom: 2px solid transparent;
            color: var(--muted-foreground);
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .tab:hover {
            color: var(--foreground);
        }
        
        .tab.active {
            color: var(--primary);
            border-bottom-color: var(--primary);
        }
        
        .main {
            padding: 2rem 0;
        }
        
        .card {
            background-color: var(--background);
            border-radius: var(--radius);
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            padding: 1.5rem;
            margin-bottom: 2rem;
        }
        
        h1 {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        h2 {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            margin-top: 1.5rem;
        }
        
        h3 {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
        }
        
        p {
            margin-bottom: 1rem;
        }
        
        .risk-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .risk-card {
            background-color: var(--background);
            border-radius: var(--radius);
            border: 1px solid var(--border);
            padding: 1.25rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        }
        
        .risk-card h3 {
            display: flex;
            align-items: center;
            font-size: 1rem;
            margin-bottom: 1rem;
            gap: 0.5rem;
        }
        
        .risk-card .icon {
            background-color: var(--primary);
            color: var(--primary-foreground);
            width: 1.75rem;
            height: 1.75rem;
            border-radius: 9999px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .risk-value {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }
        
        .high-risk {
            color: #dc2626;
        }
        
        .medium-risk {
            color: #ca8a04;
        }
        
        .low-risk {
            color: #16a34a;
        }
        
        .risk-label {
            font-size: 0.875rem;
            color: var(--muted-foreground);
            margin-bottom: 1rem;
        }
        
        .risk-summary {
            padding: 2rem;
            background-color: var(--background);
            border-radius: var(--radius);
            border: 1px solid var(--border);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .risk-meter {
            height: 0.5rem;
            background: linear-gradient(to right, #16a34a, #ca8a04, #dc2626);
            border-radius: 9999px;
            margin-top: 1.5rem;
            position: relative;
        }
        
        .risk-indicator {
            position: absolute;
            top: -0.25rem;
            width: 1rem;
            height: 1rem;
            background-color: var(--foreground);
            border: 2px solid white;
            border-radius: 9999px;
            transform: translateX(-50%);
        }
        
        /* Insurance Premium Box Styles */
        .insurance-premium-box {
            background: #f8fafc;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1.5rem;
            margin-top: 2rem;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        
        .risk-tier {
            font-size: 1.25rem;
            font-weight: 600;
            margin: 0.75rem 0;
            display: inline-block;
            padding: 0.35rem 1rem;
            border-radius: 9999px;
        }
        
        .critical-tier {
            background-color: #fef2f2;
            color: #dc2626;
        }
        
        .high-tier {
            background-color: #fff7ed;
            color: #ea580c;
        }
        
        .medium-tier {
            background-color: #fefce8;
            color: #ca8a04;
        }
        
        .low-tier {
            background-color: #f0fdf4;
            color: #16a34a;
        }
        
        .premium-range {
            font-size: 1.1rem;
            margin: 0.75rem 0;
            color: var(--foreground);
        }
        
        .premium-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--foreground);
        }
        
        .premium-note {
            font-size: 0.875rem;
            color: var(--muted-foreground);
            margin-top: 0.5rem;
        }
        
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: var(--radius);
            font-weight: 500;
            padding: 0.5rem 1rem;
            transition: all 0.2s;
            font-size: 0.875rem;
            line-height: 1.5;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            cursor: pointer;
            text-decoration: none;
        }
        
        .btn-primary {
            background-color: var(--primary);
            color: var(--primary-foreground);
        }
        
        .btn-primary:hover {
            background-color: var(--primary-hover);
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .risk-grid {
                grid-template-columns: 1fr;
            }
            
            .header-inner {
                flex-direction: column;
                height: auto;
                padding: 1rem 0;
                gap: 1rem;
            }
            
            .tabs {
                width: 100%;
                overflow-x: auto;
                padding: 0;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="header-inner">
                <a href="/" class="logo">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z" />
                    </svg>
                    CardiaLink Quantify
                </a>
            </div>
        </div>
        <div class="tabs">
            <a href="/heart" class="tab {{ 'active' if active_tab == 'heart' else '' }}">Heart Disease</a>
            <a href="/kidney" class="tab {{ 'active' if active_tab == 'kidney' else '' }}">Kidney Disease</a>
            <a href="/diabetes" class="tab {{ 'active' if active_tab == 'diabetes' else '' }}">Diabetes</a>
            <a href="/results" class="tab {{ 'active' if active_tab == 'results' else '' }}">Combined Results</a>
        </div>
    </header>
    
    <main class="main">
        <div class="container">
            <h1>Your Comprehensive Health Risk Assessment</h1>
            
            <p>This assessment combines data from multiple health evaluations to provide a comprehensive view of your overall risk profile. Below you can see both your individual risk assessments and your combined risk score.</p>
            
            <h2>Individual Risk Assessments</h2>
            
            <div class="risk-grid">
                <div class="risk-card">
                    <h3>
                        <span class="icon">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z" />
                            </svg>
                        </span>
                        Heart Disease Risk
                    </h3>
                    <div class="risk-value {{ 'high-risk' if heart_risk > 0.7 else 'medium-risk' if heart_risk > 0.3 else 'low-risk' }}">
                        {{ "%.1f"|format(heart_risk*100) }}%
                    </div>
                    <div class="risk-label">
                        {{ "High Risk" if heart_risk > 0.7 else "Medium Risk" if heart_risk > 0.3 else "Low Risk" }}
                    </div>
                </div>
                
                <div class="risk-card">
                    <h3>
                        <span class="icon">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M12 14c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5z" />
                                <path d="M18.6 18.6c-.4.2-.8.3-1.3.3h-2.3L17.3 15" />
                                <path d="M5.4 18.6c.4.2.8.3 1.3.3h2.3L6.7 15" />
                                <path d="M12 14c-2.7 0-8 1.3-8 4v2h16v-2c0-2.7-5.3-4-8-4z" />
                            </svg>
                        </span>
                        Kidney Disease Risk
                    </h3>
                    <div class="risk-value {{ 'high-risk' if kidney_risk > 0.7 else 'medium-risk' if kidney_risk > 0.3 else 'low-risk' }}">
                        {{ "%.1f"|format(kidney_risk*100) }}%
                    </div>
                    <div class="risk-label">
                        {{ "High Risk" if kidney_risk > 0.7 else "Medium Risk" if kidney_risk > 0.3 else "Low Risk" }}
                    </div>
                </div>
                
                <div class="risk-card">
                    <h3>
                        <span class="icon">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M7.2 7a2.5 2.5 0 0 0 3.4 2.5" />
                                <path d="M17 7a2.5 2.5 0 0 1-3.4 2.5" />
                                <path d="M19 11h.01" />
                                <path d="M17 15h.01" />
                                <path d="M14 13h.01" />
                                <path d="M13 17h.01" />
                                <path d="M9 13h.01" />
                                <path d="M6 15h.01" />
                                <path d="M7 11a7 7 0 0 1 10 0" />
                                <path d="M11 20.93c-1.73-.3-3.4-1-5-2.93" />
                                <path d="M13 20.93c1.73-.3 3.4-1 5-2.93" />
                            </svg>
                        </span>
                        Diabetes Risk
                    </h3>
                    <div class="risk-value {{ 'high-risk' if diabetes_risk > 0.7 else 'medium-risk' if diabetes_risk > 0.3 else 'low-risk' }}">
                        {{ "%.1f"|format(diabetes_risk*100) }}%
                    </div>
                    <div class="risk-label">
                        {{ "High Risk" if diabetes_risk > 0.7 else "Medium Risk" if diabetes_risk > 0.3 else "Low Risk" }}
                    </div>
                </div>
            </div>
            
            <h2>Comprehensive Risk Profile</h2>
            
            <div class="card">
                <div class="risk-summary">
                    <h3>Overall Risk Assessment</h3>
                    <div class="risk-value {{ 'high-risk' if combined_risk > 0.7 else 'medium-risk' if combined_risk > 0.3 else 'low-risk' }}">
                        {{ "%.1f"|format(combined_risk*100) }}%
                    </div>
                    <div class="risk-label">
                        {{ "High Risk" if combined_risk > 0.7 else "Medium Risk" if combined_risk > 0.3 else "Low Risk" }}
                    </div>
                    
                    <!-- Add insurance premium information -->
                    <div class="insurance-premium-box">
                        <h3>Insurance Premium Estimate</h3>
                        <div class="risk-tier {{ 'critical-tier' if risk_tier == 'Critical' else 'high-tier' if risk_tier == 'High' else 'medium-tier' if risk_tier == 'Medium' else 'low-tier' }}">
                            {{ risk_tier }} Risk Tier
                        </div>
                        <div class="premium-range">
                            <span class="premium-value">${{ min_premium }} - ${{ max_premium }}</span> per year
                        </div>
                        <div class="premium-note">
                            Based on your combined health risk assessment
                        </div>
                    </div>
                    
                    <div class="risk-meter">
                        <div class="risk-indicator" style="left: {{ combined_risk*100 }}%;"></div>
                    </div>
                </div>
                
                <p>This assessment is based on multiple health metrics and provides an estimate of your overall health risk status. Our risk assessment algorithm takes into account both individual risk factors and their combined effects.</p>
                
                <div style="text-align: center; margin-top: 2rem;">
                    <a href="/" class="btn btn-primary">Back to Home</a>
                </div>
            </div>
        </div>
    </main>
</body>
</html>
"""

@app.route('/results', methods=['GET'])
def results():
    # Get risk scores from session or set default values
    heart_risk = session.get('heart_risk', 0)
    kidney_risk = session.get('kidney_risk', 0)
    diabetes_risk = session.get('diabetes_risk', 0)
    
    # Calculate weighted risk
    weighted_risk = (
        (heart_risk * heart_weight) +
        (kidney_risk * kidney_weight) +
        (diabetes_risk * diabetes_weight)
    )
    
    # Check if any individual risk is extremely high (>90%)
    has_extremely_high_risk = any(risk > 0.9 for risk in [heart_risk, kidney_risk, diabetes_risk])
    
    # If any risk is extremely high, ensure the combined risk is at least 0.9
    if has_extremely_high_risk and weighted_risk < 0.9:
        weighted_risk = max(weighted_risk, 0.9)  # Ensure minimum 90% risk
    
    # Calculate insurance premium tier and range
    risk_tier, min_premium, max_premium = calculate_insurance_premium(weighted_risk)
    
    # Store risk scores in session
    session['combined_risk'] = weighted_risk
    
    print(f"Individual risks - Heart: {heart_risk}, Kidney: {kidney_risk}, Diabetes: {diabetes_risk}")
    print(f"Combined risk score (weighted): {weighted_risk}")
    print(f"Insurance Risk Tier: {risk_tier}, Premium Range: ${min_premium}-${max_premium}")
    
    return render_template_string(RESULTS_TEMPLATE,
                                active_tab='results',
                                heart_risk=heart_risk,
                                kidney_risk=kidney_risk,
                                diabetes_risk=diabetes_risk,
                                combined_risk=weighted_risk,
                                risk_tier=risk_tier,
                                min_premium=min_premium,
                                max_premium=max_premium) 