from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def generate_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title = Paragraph("Rapport d'Analyse d'Option", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Data
    text = f"""
    <b>Paramètres:</b><br/>
    Sous-jacent: {data['ticker'] if data['ticker'] else data['S0']}<br/>
    Strike: {data['K']}<br/>
    Maturité: {data['T']} ans<br/>
    Taux sans risque: {data['r']*100:.1f}%<br/>
    Volatilité: {data['sigma']*100:.1f}%<br/>
    Type d'option: {data['option_type'].capitalize()}
    """
    story.append(Paragraph(text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Results
    text = f"""
    <b>Résultats:</b><br/>
    Prix Black-Scholes: {data['bs_price']:.2f}<br/>
    Prix Monte Carlo: {data['mc_price']:.2f}<br/><br/>
    
    <b>Grecques:</b><br/>
    Delta {data['option_type'].capitalize()}: {data['greeks'][f'delta_{data["option_type"]}']:.4f}<br/>
    Gamma: {data['greeks']['gamma']:.4f}<br/>
    Vega: {data['greeks']['vega']:.4f}<br/>
    Theta {data['option_type'].capitalize()}: {data['greeks'][f'theta_{data["option_type"]}']:.4f}/jour<br/>
    Rho {data['option_type'].capitalize()}: {data['greeks'][f'rho_{data["option_type"]}']:.4f}%/point
    """
    story.append(Paragraph(text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Graphics
    img = Image('static/plots/mc_convergence.png', 7*inch, 5*inch)
    story.append(img)
    doc.build(story)
    
    with open('static/report.pdf', 'wb') as f:
        f.write(buffer.getvalue())
    
    buffer.seek(0)
    return buffer