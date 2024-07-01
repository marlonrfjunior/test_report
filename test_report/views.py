

def generate_report_html(report_data):
    sidebar_html = generate_sidebar(report_data)
    scenario_details_html = generate_scenario_details(report_data)

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Test Report</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        <script src="https://cdn.jsdelivr.net/npm/chart.js@3.7.0/dist/chart.min.js"></script>
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 20px;
            }}
            .sidebar {{
                height: 100%;
                width: 300px;
                position: fixed;
                top: 0;
                left: 0;
                background-color: #f8f9fa;
                padding: 20px;
                overflow-x: hidden;
                border-right: 1px solid #ddd;
            }}
            .sidebar ul.nav {{
                list-style-type: none;
                padding-left: 0;
            }}
            .sidebar ul.nav li {{
                margin-bottom: 10px;
            }}
            .sidebar ul.nav li a {{
                display: block;
                padding: 10px 15px;
                color: #333;
                text-decoration: none;
                transition: background-color 0.3s;
            }}
            .sidebar ul.nav li a:hover {{
                background-color: #ddd;
            }}
            .content {{
                margin-left: 320px;
                padding: 20px;
            }}
            .chart-container {{
                width: 100%;
                height: 300px;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        {sidebar_html}
        <div class="content">
            <h1 class="mt-4 mb-4">Test Report</h1>
            <div id="cenarios">
                {scenario_details_html}
            </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    """
import json


def generate_scenario_details(report_data):
    html = ""
    for scenario in report_data["scenarios"]:
        html += f"""
            <div class="card mb-4">
                <div class="card-header" data-toggle="collapse" data-target="#cenario_{scenario["uuid"]}">
                    <div class="row">
                        <div class="col-8">
                            <h5 class="mb-0">
                                <i class="fas fa-caret-right mr-2"></i> 
                                <i class="{'text-success' if scenario["status"] else 'text-danger'} fas fa-{'check' if scenario["status"] else 'times'}-circle"></i>
                                {scenario["name"]}
                            </h5>
                        </div>
                        <div class="col-4">
                            <h6 class="mb-0 d-flex justify-content-end align-items-center">
                                {(scenario['formated_execution_time'])}
                            </h6>
                        </div>
                    </div>
                </div>
                <div id="cenario_{scenario["uuid"]}" class="collapse">
                    <div class="card-body">
        """
        for test_case in scenario["test_cases"]:
            html += generate_test_case_details(test_case)
        html += """
                    </div>
                </div>
            </div>
        """
    return html
import json

def generate_sidebar(report_data):
    labels_resumo = ['Successful Tests', 'Failed tests']
    dados_resumo = [int(report_data["total_tests"] - report_data["total_failures"]), int(report_data["total_failures"])]
    cores_resumo = ['#28a745', '#dc3545']

    labels_tempo_execucao = [scenario["name"] for scenario in report_data["scenarios"]]
    dados_tempo_execucao = [scenario["execution_time"] for scenario in report_data["scenarios"]]
    cores_tempo_execucao = ['#007bff', '#6610f2', '#6f42c1', '#17a2b8', '#28a745']

    labels_resumo_json = json.dumps(labels_resumo)
    dados_resumo_json = json.dumps(dados_resumo)
    cores_resumo_json = json.dumps(cores_resumo)
    labels_tempo_execucao_json = json.dumps(labels_tempo_execucao)
    dados_tempo_execucao_json = json.dumps(dados_tempo_execucao)
    cores_tempo_execucao_json = json.dumps(cores_tempo_execucao)

    return f"""
    <div class="sidebar">
{ '<img src="' + report_data["image_header_path"] +'" class="img-fluid mb-4" alt="Imagem de topo">' if report_data["image_header_path"] is not None else ""}
        <div class="mt-4">
            <h5 class = "font-weight-bold">Test summary</h5>
            <canvas id="resumoTestesChart"></canvas>
        </div>
        <div class="mt-4">
            <h5 class = "font-weight-bold">Execution Time </h5>
            <p>{report_data["total_execution_time"]} (mm:ss:ms)</p>
            <canvas id="tempoExecucaoChart"></canvas>
        </div>
    </div>
    <script>
        var ctxResumoTestes = document.getElementById('resumoTestesChart').getContext('2d');
        var resumoTestesChart = new Chart(ctxResumoTestes, {{
            type: 'doughnut',
            data: {{
                labels: {labels_resumo_json},
                datasets: [{{
                    label: 'Test summary',
                    data: {dados_resumo_json},
                    backgroundColor: {cores_resumo_json},
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'top',
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(tooltipItem) {{
                                return ' ' + tooltipItem.label + ': ' + tooltipItem.raw.toFixed(1);
                            }}
                        }}
                    }}
                }}
            }}
        }});

        var ctxTempoExecucao = document.getElementById('tempoExecucaoChart').getContext('2d');
        var tempoExecucaoChart = new Chart(ctxTempoExecucao, {{
            type: 'bar',
            data: {{
                labels: {labels_tempo_execucao_json},
                datasets: [{{
                    label: 'Execution Time by Scenario(s)',
                    data: {dados_tempo_execucao_json},
                    backgroundColor: {cores_tempo_execucao_json},
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        display: false,
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(tooltipItem) {{
                                return ' ' + tooltipItem.label + ': ' + tooltipItem.raw.toFixed(1) + 's';
                            }}
                        }}
                    }}
                }},
                scales: {{
                    x: {{
                        stacked: true
                    }},
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
    </script>
    """
def generate_step_details(step):
    screenshot_html = f'<img src="data:image/png;base64,{step["screenshot"]}" class="img-fluid mt-2 mb-2" style="max-width: 400px;"/><br>' if step["screenshot"] else ''
    return f"""
        <div class="card mb-2">
            <div class="card-header" data-toggle="collapse" data-target="#step_{step["uuid"]}">
                <div class="row">
                    <div class="col-8">
                        <p class="mb-0">
                            <i class="fas fa-caret-right mr-2"></i>
                            <i class="{'text-success' if step["status"] else 'text-danger'} fas fa-{'check' if step["status"] else 'times'}-circle"></i>
                            {step["name"]}
                        </p>
                    </div>
                    <div class="col-4">
                        <p class="mb-0 d-flex justify-content-end align-items-center">
                            {(step['formated_execution_time'])}
                        </p>
                    </div>
                </div>
            </div>
            <div id="step_{step["uuid"]}" class="collapse">
                <div class="card-body">
                        <h6 class="mb-0 d-flex align-items-center">
                            {(step['description'])}
                        </h6>
                    {screenshot_html}
                </div>
            </div>
        </div>
    """


def generate_test_case_details(test_case):
    html = f"""
        <div class="card mb-3">
            <div class="card-header" data-toggle="collapse" data-target="#test_case_{test_case["uuid"]}">
                <div class="row">
                    <div class="col-8">
                        <h6 class="mb-0 d-flex justify-content-start align-items-center">
                            <i class="fas fa-caret-right mr-2"></i>
                            <i class="{'text-success' if test_case["status"] else 'text-danger'} fas fa-{'check' if test_case["status"] else 'times'}-circle"></i>
                            <span class="ml-2">{test_case["name"]}</span>
                        </h6>
                    </div>
                    <div class="col-4">
                        <h6 class="mb-0 d-flex justify-content-end align-items-center">
                            {(test_case['formated_execution_time'])}
                        </h6>
                    </div>
                </div>
            </div>
            <div id="test_case_{test_case["uuid"]}" class="collapse">
                <div class="card-body">
    """
    for step in test_case["steps"]:
        html += generate_step_details(step)
    html += """
                </div>
            </div>
        </div>
    """
    return html
