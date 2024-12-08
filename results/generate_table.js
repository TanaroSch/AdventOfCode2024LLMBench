const fs = require('fs');

// Function to generate the HTML table from data.json
function generateTable() {
    try {
        // Read and parse the data.json file
        const data = JSON.parse(fs.readFileSync('data.json', 'utf8'));

        // Start building the HTML
        let html = `
<style>
table {
    border-collapse: collapse;
    font-family: Arial, sans-serif;
    font-size: 14px;
    margin: 20px 0;
    width: max-content;
}

th, td {
    border: 1px solid #666;
    padding: 2px 4px;
    text-align: center;
}

th {
    background-color: #4472C4;
    color: white;
}

/* Top header row cells (model names) */
tr:first-child th {
    padding: 4px 8px;
}

/* Second header row cells (P1, P2, E) */
tr:nth-child(2) th {
    width: 30px;
    padding: 2px;
}

/* First column (Day) */
td:first-child, th:first-child {
    width: 30px;
}

/* Data cells width */
td {
    width: 30px;
}

/* Value colors */
.v1 { background-color: #90EE90; }  /* Light green */
.v2 { background-color: #98FB98; }  /* Pale green */
.v3 { background-color: #FFE4B5; }  /* Light orange */
.v4 { background-color: #FFA07A; }  /* Light salmon */
.v5 { background-color: #FFA500; }  /* Orange */
.vx { background-color: #FFB6C6; }  /* Light red */
</style>

<table>
    <tr>
        <th rowspan="2">Day</th>`;

        // Add model headers
        data.models.forEach(model => {
            html += `
        <th colspan="3">${model}</th>`;
        });

        // Add subheaders
        html += `
    </tr>
    <tr>`;
        data.models.forEach(() => {
            html += `
        <th>P1</th><th>P2</th><th>E</th>`;
        });
        html += `
    </tr>`;

        // Add data rows
        data.days.forEach(day => {
            html += `
    <tr>
        <td>${day.day}</td>`;
            data.models.forEach(model => {
                const result = day.results[model];
                const p1Class = getCellClass(result.part1);
                const p2Class = getCellClass(result.part2);
                const errors = result.errors ? result.errors.join(',') : '';
                
                html += `
        <td class="${p1Class}">${result.part1}</td>
        <td class="${p2Class}">${result.part2}</td>
        <td>${errors}</td>`;
            });
            html += `
    </tr>`;
        });

        html += `
</table>`;

        // Write to results.html
        fs.writeFileSync('results.html', html);
        console.log('Generated results.html');
        
    } catch (error) {
        console.error('Error generating table:', error);
    }
}

function getCellClass(value) {
    switch(value) {
        case '1': return 'v1';
        case '2': return 'v2';
        case '3': return 'v3';
        case '4': return 'v4';
        case '5': return 'v5';
        case 'X':
        case '-': return 'vx';
        default: return '';
    }
}

// Run the generation
generateTable();