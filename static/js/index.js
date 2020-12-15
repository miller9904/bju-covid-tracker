Plotly.d3.json("/api/v1/entries/all?sort=ascending", function (err, data) {


    function isolations(data) {
        return data.map(function (data) { return data.studentIsolation + data.facStaffIsolation; });
    }

    function hospitalizationTrace(data) {
        return data.map(function (data) { return data.studentHospitalization + data.facStaffHospitalization; });
    }

    function date(data) {
        return data.map(function (data) {

            var date = new Date();
            var dateStr = data.date.toString();

            date.setFullYear(dateStr.substring(0, 4));
            date.setMonth(dateStr.substring(4, 6) - 1);
            date.setDate(dateStr.substring(6, 8) - 1);
            date.setHours(24, 0, 0, 0);

            return date.toISOString();
        });
    }

    var isolationTrace = {
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Isolations',
        x: date(data),
        y: isolations(data),
        line: {
            color: '#0B4F6C',
            shape: 'spline',
            width: 2
        }
    }

    var hospitalizationTrace = {
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Hospitalizations',
        x: date(data),
        y: hospitalizationTrace(data),
        line: {
            color: '#714955',
            shape: 'spline',
            width: 2
        }
    }

    var layout = {
        showlegend: true,
        legend: {
            x: 1,
            xanchor: 'right',
            y: 1
        },
        font: {
            family: 'Roboto'
        },

        xaxis: {
            type: 'date',
            tickformat: '%b %e',
            tickfont: {
                family: 'Roboto'
            },
            automargin: true,
            rangeselector: {buttons: [
                {
                  count: 1,
                  label: '1m',
                  step: 'month',
                  stepmode: 'backward'
                },
                {
                  count: 6,
                  label: '6m',
                  step: 'month',
                  stepmode: 'backward'
                },
                {step: 'all'}
              ]},
        },

        yaxis: {
            automargin: true
        },

        margin: {
            l: 10,
            r: 10,
            b: 50,
            t: 50,
            pad: 4
          },
    }

    var config = {
        responsive: true,
        displaylogo: false
    }

    Plotly.newPlot('activeCasesGraph', [isolationTrace, hospitalizationTrace], layout, config);
})