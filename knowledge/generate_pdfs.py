import os
import struct

def create_simple_pdf(title: str, text_content: str, filename: str):
    """Generates a valid minimal PDF file with text content."""
    lines = text_content.strip().split("\n")
    stream_content = "BT\n/F1 12 Tf\n36 750 Td\n14 TL\n"
    stream_content += f"({title}) Tj T*\n\n"
    
    for line in lines:
        cleaned_line = line.replace("(", "\\(").replace(")", "\\)")
        stream_content += f"({cleaned_line}) Tj T*\n"
    stream_content += "ET\n"

    stream_len = len(stream_content)

    pdf_body = f"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kinds [3 0 R] /Count 1 /Kids [3 0 R] >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>
endobj
4 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
5 0 obj
<< /Length {stream_len} >>
stream
{stream_content}endstream
endobj
xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000133 00000 n
0000000257 00000 n
0000000332 00000 n
trailer
<< /Size 6 /Root 1 0 R >>
startxref
410
%%EOF
"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="latin1") as f:
        f.write(pdf_body)

KNOWLEDGE_DOCUMENTS = {
    "air_quality_guidelines.pdf": {
        "title": "WHO and EPA Global Air Quality Guidelines (2024)",
        "text": """Document ID: REF-AQG-2024
Source: World Health Organization & US Environmental Protection Agency
Topic: Air Quality Index Thresholds and Target Exposure Levels

Key Guidelines:
1. PM2.5 Annual Target: 5 ug/m3. 24-hour target: 15 ug/m3.
2. PM10 Annual Target: 15 ug/m3. 24-hour target: 45 ug/m3.
3. Nitrogen Dioxide (NO2) 24-hour target: 25 ug/m3.
4. Ozone (O3) 8-hour peak target: 100 ug/m3.
5. Sulfur Dioxide (SO2) 24-hour target: 40 ug/m3.

AQI Scale Standard:
- 0 to 50 (Good): Air quality is satisfactory.
- 51 to 100 (Moderate): Acceptable quality for general public.
- 101 to 150 (Unhealthy for Sensitive Groups): Sensitive groups may experience health effects.
- 151 to 200 (Unhealthy): Everyone may begin to experience health effects.
- 201 to 300 (Very Unhealthy): Health alert; risk of severe impacts.
- 301+ (Hazardous): Health warning of emergency conditions."""
    },
    "pollution_precautions.pdf": {
        "title": "General Public Pollution Precautions & Action Guide",
        "text": """Document ID: REF-PRE-2024
Source: Center for Environmental Health & Protection
Topic: Practical Precautions for Elevated AQI Levels

Recommended Actions by AQI Tier:
1. Moderate (AQI 51-100):
   - Unusually sensitive individuals should consider limiting prolonged outdoor exertion.
2. Unhealthy for Sensitive Groups (AQI 101-150):
   - Children, elderly, and individuals with respiratory conditions should reduce outdoor activity.
   - Wear N95 or KN95 respirators when near heavy traffic corridors.
3. Unhealthy (AQI 151-200):
   - Avoid prolonged or heavy exertion outdoors.
   - Keep windows closed and run indoor air purifiers with HEPA filtration.
   - Reschedule outdoor athletic events to early morning or indoor facilities.
4. Very Unhealthy & Hazardous (AQI > 200):
   - Remain indoors with high-efficiency particulate air filtration.
   - Avoid all strenuous physical activity outdoors."""
    },
    "outdoor_activity_guidance.pdf": {
        "title": "Outdoor Physical Activity and Athletic Guidance",
        "text": """Document ID: REF-OUT-2024
Source: Sports Medicine & Environmental Health Institute
Topic: Athletic Training, Exercise, and Outdoor Activity Safety

Exercise Risk Matrix:
1. Ventilation Rate Impact: Strenuous exercise increases inhalation of ambient pollutants by 4x to 8x.
2. AQI <= 50: All outdoor physical activities, running, and competitive sports safe.
3. AQI 51-100: Safe for healthy athletes. Monitor athletes with asthma or exercise-induced bronchospasm.
4. AQI 101-150: Reduce duration and intensity of outdoor workouts. Substitute high-intensity cardio with indoor training.
5. AQI > 150: Cancel or move all outdoor endurance sports and school athletic practices indoors.
6. Timing Optimization: Avoid training near major highways during 07:00-09:00 and 17:00-19:00 peak traffic hours."""
    },
    "indoor_air_quality.pdf": {
        "title": "Indoor Air Quality and Air Purification Protocols",
        "text": """Document ID: REF-IND-2024
Source: Indoor Air Protection Bureau
Topic: HEPA Air Purifiers, Ventilation, and Indoor Source Management

Indoor Protection Strategies:
1. Filtration Standards: Use True HEPA air purifiers (H13 or H14 rated) capturing 99.97% of particles down to 0.3 microns.
2. Recirculation Mode: Set HVAC systems to internal recirculation during outdoor pollution spikes.
3. Sealing Protocols: Close windows, external doors, and fireplace dampers when outdoor AQI exceeds 100.
4. Indoor Source Avoidance: Do not burn candles, incense, or wood during high outdoor pollution events.
5. MERV Ratings: Install MERV 13 or higher filters in central HVAC heating and cooling systems."""
    },
    "children_air_quality_guidance.pdf": {
        "title": "Children and School Air Quality Safety Guidelines",
        "text": """Document ID: REF-CHI-2024
Source: Pediatric Health Association & School Safety Board
Topic: Protecting Infants, Children, and Students from Air Pollution

Pediatric Risk Factors:
1. Higher Respiratory Rate: Children breathe 50% more air per pound of body weight than adults.
2. Developing Lungs: Inhaled particulates impair pulmonary alveolar development.

School Recess Guidelines:
- AQI 0-50: Full outdoor recess and sports allowed.
- AQI 51-100: Normal outdoor activity; observe asthmatic children closely.
- AQI 101-150: Limit prolonged outdoor exertion to 15 minutes; asthmatic children stay indoors.
- AQI 151-200: Move all recess, PE classes, and after-school sports indoors.
- AQI > 200: Full outdoor activity cancellation; activate classroom HEPA purifiers."""
    },
    "elderly_air_quality_guidance.pdf": {
        "title": "Elderly and Cardiovascular Health Safety Protocol",
        "text": """Document ID: REF-ELD-2024
Source: Geriatric Health Council & Cardiovascular Protection Association
Topic: Air Pollution Precautions for Seniors and Cardiac Patients

Health Considerations:
1. Fine Particulate Matter (PM2.5) penetrates deep into the bloodstream, triggering vascular inflammation and arrhythmia.
2. Seniors with hypertension, coronary artery disease, or COPD are at elevated risk during particulate spikes.

Safety Recommendations:
- Monitor daily local AQI and particulate readings prior to outdoor plans.
- When AQI exceeds 100, refrain from outdoor yard work, gardening, or long walks.
- Keep emergency respiratory medication (e.g. quick-relief inhalers) accessible.
- Maintain adequate hydration and remain in air-conditioned, HEPA-filtered indoor environments."""
    },
    "outdoor_worker_guidance.pdf": {
        "title": "Occupational Health Guidance for Outdoor Workers",
        "text": """Document ID: REF-WRK-2024
Source: Occupational Safety & Environmental Health Administration
Topic: Construction, Delivery, Municipal, and Agricultural Worker Safety

Occupational Protection Mandates:
1. Employer Responsibilities: Monitor ambient air quality at job sites hourly when AQI exceeds 100.
2. Respiratory Protection: Provide NIOSH-approved N95 or KN95 respirators free of charge when PM2.5 exceeds 35.4 ug/m3 (AQI > 100).
3. Work-Rest Cycles: Implement mandatory 15-minute indoor rest breaks per hour in air-conditioned break areas when AQI exceeds 150.
4. Workload Adjustment: Shift heavy manual labor tasks to early morning hours when ozone and PM levels are lowest."""
    },
    "pollution_health_information.pdf": {
        "title": "Pathophysiology and Health Impacts of Airborne Pollutants",
        "text": """Document ID: REF-HLT-2024
Source: Global Pulmonary & Environmental Medicine Journal
Topic: Physiological Effects of PM2.5, PM10, NO2, O3, and SO2

Pollutant Pathophysiology:
1. PM2.5 (Fine Particles): Inhaled into pulmonary alveoli; translocates to bloodstream; triggers systemic oxidation, arterial stiffness, and myocardial strain.
2. PM10 (Coarse Particles): Deposited in upper airways; causes throat irritation, coughing, and bronchitis exacerbation.
3. Nitrogen Dioxide (NO2): Causes bronchial airway inflammation, asthma exacerbation, and reduced lung capacity.
4. Ground-Level Ozone (O3): Powerful oxidant that damages lung lining tissue, causing chest tightness and deep breathing discomfort.
5. Sulfur Dioxide (SO2): Induces bronchoconstriction in asthmatic individuals within minutes of exposure."""
    },
    "emergency_guidance.pdf": {
        "title": "Severe Air Pollution & Wildfire Smoke Emergency Protocol",
        "text": """Document ID: REF-EMG-2024
Source: National Emergency Management Agency
Topic: Emergency Protocols for Wildfire Smoke and Industrial Pollution Disasters

Emergency Response Action Steps:
1. Hazardous AQI (AQI > 300): Activate emergency clean air shelters.
2. Clean Room Setup: Designate an interior room with zero windows or single sealed window; run continuous HEPA purifiers.
3. Mask Mandate: Fit-tested N95, KN95, or elastomeric respirators required for any necessary brief outdoor transit.
4. HVAC Isolation: Close fresh air intakes on building ventilation systems immediately.
5. Health Triage: Seek emergency medical care immediately for severe shortness of breath, persistent chest pressure, or cyanosis."""
    }
}

def generate_all_knowledge_pdfs():
    out_dir = os.path.join(os.path.dirname(__file__))
    for fname, doc_info in KNOWLEDGE_DOCUMENTS.items():
        filepath = os.path.join(out_dir, fname)
        create_simple_pdf(doc_info["title"], doc_info["text"], filepath)
        print(f"[PDF Generator] Created {fname} at {filepath}")

if __name__ == "__main__":
    generate_all_knowledge_pdfs()
