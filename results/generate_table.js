const fs = require('fs');

function calculateModelScores(data) {
    const scores = {};
    const totalDays = data.days.length;

    data.models.forEach(model => {
        let successfulPart1 = 0;
        let successfulPart2 = 0;
        let totalAttemptsPart1 = 0;
        let totalAttemptsPart2 = 0;
        let attemptedPart1 = 0;
        let attemptedPart2 = 0;

        data.days.forEach(day => {
            const result = day.results[model];
            
            if (result.part1 !== 'X') {
                successfulPart1++;
                totalAttemptsPart1 += parseInt(result.part1);
                attemptedPart1++;
            }
            
            if (result.part2 !== 'X' && result.part2 !== '-') {
                successfulPart2++;
                totalAttemptsPart2 += parseInt(result.part2);
                attemptedPart2++;
            }
        });

        const successRate = ((successfulPart1 + successfulPart2) / (2 * totalDays)) * 100;
        const efficiencyRate = (
            (attemptedPart1 > 0 ? attemptedPart1 / totalAttemptsPart1 : 0) +
            (attemptedPart2 > 0 ? attemptedPart2 / totalAttemptsPart2 : 0)
        ) * 50;
        const finalScore = (0.7 * successRate) + (0.3 * efficiencyRate);

        scores[model] = {
            successRate,
            efficiencyRate,
            finalScore
        };
    });

    return scores;
}

function getCellColor(value) {
    switch(value) {
        case '1': return '#90EE90';  // Light green
        case '2': return '#98FB98';  // Pale green
        case '3': return '#FFE4B5';  // Light orange
        case '4': return '#FFA07A';  // Light salmon
        case '5': return '#FFA500';  // Orange
        case 'X':
        case '-': return '#FFB6C6';  // Light red
        default: return '#FFFFFF';    // White
    }
}

function generateTables() {
    try {
        const data = JSON.parse(fs.readFileSync('data.json', 'utf8'));
        const scores = calculateModelScores(data);
        const sortedModels = [...data.models].sort((a, b) => 
            scores[b].finalScore - scores[a].finalScore
        );

        // Generate rankings table
        let rankingsHtml = `<table>
    <tr>
        <th align="center">Rank</th>
        <th align="center">Model</th>
        <th align="center">Success Rate</th>
        <th align="center">Efficiency Rate</th>
        <th align="center">Final Score</th>
    </tr>\n`;

        sortedModels.forEach((model, index) => {
            const score = scores[model];
            rankingsHtml += `    <tr>
        <td align="center">${index + 1}</td>
        <td align="center">${model}</td>
        <td align="center">${score.successRate.toFixed(1)}%</td>
        <td align="center">${score.efficiencyRate.toFixed(1)}%</td>
        <td align="center">${score.finalScore.toFixed(1)}</td>
    </tr>\n`;
        });

        rankingsHtml += '</table>\n';
        fs.writeFileSync('rankings.html', rankingsHtml);

        // Generate results table
        let resultsHtml = `<table>
    <tr>
        <th align="center" rowspan="2">Day</th>`;

        sortedModels.forEach(model => {
            resultsHtml += `
        <th align="center" colspan="3">${model}</th>`;
        });

        resultsHtml += `
    </tr>
    <tr>`;
        
        sortedModels.forEach(() => {
            resultsHtml += `
        <th align="center">P1</th><th align="center">P2</th><th align="center">E</th>`;
        });
        
        resultsHtml += `
    </tr>\n`;

        data.days.forEach(day => {
            resultsHtml += `    <tr>
        <td align="center">${day.day}</td>`;
            sortedModels.forEach(model => {
                const result = day.results[model];
                const p1Color = getCellColor(result.part1);
                const p2Color = getCellColor(result.part2);
                const errors = result.errors ? result.errors.join(',') : '';
                
                resultsHtml += `
        <td align="center" bgcolor="${p1Color}">${result.part1}</td>
        <td align="center" bgcolor="${p2Color}">${result.part2}</td>
        <td align="center">${errors}</td>`;
            });
            resultsHtml += `
    </tr>\n`;
        });

        resultsHtml += '</table>';
        fs.writeFileSync('results.html', resultsHtml);
        
        console.log('Generated:');
        console.log('- rankings.html');
        console.log('- results.html');
        
    } catch (error) {
        console.error('Error generating tables:', error);
    }
}

generateTables();