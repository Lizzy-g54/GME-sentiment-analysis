(function() {
    const margin = {top: 20, right: 50, bottom: 40, left: 60};
    let globalComments = []; 

    const parseDate = d3.timeParse("%Y-%m-%d");
    const formatDate = d3.timeFormat("%b %d, %Y");

    // --- 高对比度配色 (High Contrast Palette) ---
    const palette = {
        Hype: "#007bff",   // 纯正蓝
        Fear: "#ff9f1c",   // 明亮橙
        Anger: "#d63031",  // 宝石红
        Noise: "#636e72",  // 炭灰色
        VolLine: "#e9ecef" // 波动率背景色
    };

    // K线图：修改为单色红色渐变 (数值越大越红)
    const colorFear = d3.scaleSequential()
        .domain([0.45, 0.75]) 
        .interpolator(d3.interpolateReds);

    const getSentColor = (s) => {
        const key = s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
        return palette[key] || "#dee2e6";
    };

    Promise.all([
        d3.csv("dataset/final_dataset_for_vis.csv"),
        d3.csv("dataset/top_comments.csv").catch(() => []) 
    ]).then(([marketData, commentData]) => {
        globalComments = commentData;

        const data = marketData.map((d, i) => {
            const date = parseDate(d.date);
            if (!date) return null;
            return {
                date: date,
                close: +d.close,
                high: +d.high,
                low: +d.low,
                open: i > 0 ? +marketData[i-1].close : +d.low,
                volatility: +d.volatility,
                fear_ratio: +d.fear_ratio,
                hype: +d.count_Hype,
                fear: +d.count_Fear,
                anger: +d.count_Anger,
                noise: +d.count_Noise
            };
        }).filter(d => d !== null);

        renderVis1(data);
        renderVis3(data);
        renderVis5(data);
    });

    function updateComments(dateObj) {
        const ds = d3.timeFormat("%Y-%m-%d")(dateObj);
        d3.select("#selected-date-display").text(formatDate(dateObj));
        
        const filtered = globalComments.filter(c => c.date === ds);
        const box = d3.select("#comment-list");
        box.selectAll("*").remove();

        if (filtered.length === 0) {
            box.append("p").attr("class", "text-muted small py-3").text("No trending comments for this date.");
            return;
        }

        filtered.forEach(c => {
            const item = box.append("div").attr("class", "comment-item");
            item.append("div").attr("class", "mb-2")
                .html(`<span class="sentiment-tag" style="background:${getSentColor(c.sentiment_label)}">${c.sentiment_label}</span> 
                       <span class="ms-2 text-muted small fw-bold">UPVOTES: ${c.score}</span>`);
            item.append("div").attr("class", "small").style("color", "#1a1a1a").style("line-height", "1.5").text(c.body);
        });
    }

    // --- VIS 1: CANDLESTICK WITH BRUSH ---
    function renderVis1(data) {
        const el = document.getElementById('vis1');
        const totalW = el.clientWidth;
        const totalH = el.clientHeight;
        
        // 重新分配空间：上方主图留大空间，下方滑动条留小空间
        const marginFocus = {top: 40, right: 50, bottom: 80, left: 60};
        const marginContext = {top: totalH - 50, right: 50, bottom: 20, left: 60};
        
        const width = totalW - marginFocus.left - marginFocus.right;
        const heightFocus = totalH - marginFocus.top - marginFocus.bottom;
        const heightContext = totalH - marginContext.top - marginContext.bottom;

        d3.select("#vis1").selectAll("*").remove(); // 清空旧图
        const svg = d3.select("#vis1").append("svg").attr("width", totalW).attr("height", totalH);

        // 限制K线不画到坐标轴外面
        svg.append("defs").append("clipPath").attr("id", "clip")
            .append("rect").attr("width", width).attr("height", heightFocus);

        // 1. 添加纯红渐变图例
        const legendWidth = 150;
        const linearGradient = svg.select("defs").append("linearGradient")
            .attr("id", "red-gradient").attr("x1", "0%").attr("y1", "0%").attr("x2", "100%").attr("y2", "0%");
        linearGradient.selectAll("stop").data([
            {offset: "0%", color: "#fee5d9"}, {offset: "50%", color: "#fb6a4a"}, {offset: "100%", color: "#cb181d"}
        ]).enter().append("stop").attr("offset", d => d.offset).attr("stop-color", d => d.color);

        const legend = svg.append("g").attr("transform", `translate(${totalW - legendWidth - marginFocus.right}, 10)`);
        legend.append("rect").attr("width", legendWidth).attr("height", 10).style("fill", "url(#red-gradient)");
        legend.append("text").attr("x", 0).attr("y", 22).style("font-size", "10px").text("Lower Fear");
        legend.append("text").attr("x", legendWidth).attr("y", 22).style("text-anchor", "end").style("font-size", "10px").text("High Fear");

        // 2. 设置双坐标系
        const x = d3.scaleTime().domain(d3.extent(data, d => d.date)).range([0, width]);
        const x2 = d3.scaleTime().domain(x.domain()).range([0, width]);
        const y = d3.scaleLinear().domain([0, d3.max(data, d => d.high)]).range([heightFocus, 0]);
        const y2 = d3.scaleLinear().domain(y.domain()).range([heightContext, 0]);

        const xAxis = d3.axisBottom(x).tickFormat(d3.timeFormat("%m/%d"));
        const xAxis2 = d3.axisBottom(x2).tickFormat(d3.timeFormat("%m/%d"));
        const yAxis = d3.axisLeft(y).ticks(5);

        const brush = d3.brushX().extent([[0, 0], [width, heightContext]]).on("brush end", brushed);

        // 3. 渲染主图 (Focus)
        const focus = svg.append("g").attr("transform", `translate(${marginFocus.left},${marginFocus.top})`);
        const focusChart = focus.append("g").attr("clip-path", "url(#clip)");
        const candleWidth = (width / data.length) * 0.6;

        const candles = focusChart.selectAll(".candle").data(data).enter().append("g").attr("class", "candle");
        
        candles.append("line").attr("class", "stem")
            .attr("x1", d => x(d.date)).attr("x2", d => x(d.date))
            .attr("y1", d => y(d.high)).attr("y2", d => y(d.low))
            .attr("stroke", "#adb5bd");

        candles.append("rect").attr("class", "body")
            .attr("x", d => x(d.date) - candleWidth/2)
            .attr("y", d => y(Math.max(d.open, d.close)))
            .attr("width", candleWidth)
            .attr("height", d => Math.max(2, Math.abs(y(d.open) - y(d.close))))
            .attr("fill", d => colorFear(d.fear_ratio))
            .on("mouseover", (event, d) => { 
                // 原来的右侧评论更新逻辑
                updateComments(d.date); 
                d3.select(event.currentTarget).attr("stroke", "#000").attr("stroke-width", 2); 
                
                // 🌟 新增 Tooltip 逻辑
                // 计算涨跌和总评论数
                const priceChange = d.close - d.open;
                const isUp = priceChange >= 0;
                const trendText = isUp ? `▲ Up ($${priceChange.toFixed(2)})` : `▼ Down ($${Math.abs(priceChange).toFixed(2)})`;
                const trendColor = isUp ? "#2ecc71" : "#ff7675"; // 涨绿跌红
                const totalPosts = d.hype + d.fear + d.anger + d.noise;

                tooltip.transition().duration(200).style("opacity", 1);
                tooltip.html(`
                    <div style="margin-bottom: 5px; border-bottom: 1px solid #555; padding-bottom: 3px;">
                        <strong>${d3.timeFormat("%b %d, %Y")(d.date)}</strong>
                    </div>
                    Market: <span style="color:${trendColor}; font-weight:bold;">${trendText}</span><br/>
                    Total Posts: <b>${totalPosts}</b><br/>
                    Fear Ratio: <b style="color:#ff9f1c;">${(d.fear_ratio * 100).toFixed(1)}%</b>
                `)
                .style("left", (event.pageX + 15) + "px")
                .style("top", (event.pageY - 28) + "px");
            })
            .on("mousemove", (event) => {
                // 让提示框跟随鼠标移动
                tooltip.style("left", (event.pageX + 15) + "px")
                       .style("top", (event.pageY - 28) + "px");
            })
            .on("mouseout", (event) => {
                // 鼠标移开时隐藏
                d3.select(event.currentTarget).attr("stroke", "none");
                tooltip.transition().duration(500).style("opacity", 0);
            });

        focus.append("g").attr("class", "axis axis--x").attr("transform", `translate(0,${heightFocus})`).call(xAxis);
        focus.append("g").attr("class", "axis axis--y").call(yAxis);
        focus.append("text")
            .attr("transform", "rotate(-90)") // 逆时针旋转 90 度
            .attr("y", -marginFocus.left + 15) // 向左平移到坐标轴外侧
            .attr("x", -(heightFocus / 2))     // 在 Y 轴上垂直居中
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .style("font-weight", "bold")
            .style("font-size", "12px")
            .text("GME Stock Price (USD)");

        // 4. 渲染底部滑动条 (Context)
        const context = svg.append("g").attr("transform", `translate(${marginContext.left},${marginContext.top})`);
        context.append("path").datum(data).attr("fill", "none").attr("stroke", "#ced4da")
            .attr("d", d3.line().x(d => x2(d.date)).y(d => y2(d.close))); // 底部画一条简易走势线
            
        context.append("g").attr("class", "axis axis--x").attr("transform", `translate(0,${heightContext})`).call(xAxis2);
        context.append("g").attr("class", "brush").call(brush).call(brush.move, x.range());

        // 5. 拖动时的动态更新逻辑
        function brushed(event) {
            const selection = event.selection || x2.range();
            x.domain(selection.map(x2.invert, x2));
            
            const visibleData = data.filter(d => d.date >= x.domain()[0] && d.date <= x.domain()[1]);
            const newMaxY = d3.max(visibleData, d => d.high) || 10;
            y.domain([0, newMaxY * 1.1]); // 动态更新Y轴最大值

            focus.select(".axis--x").call(xAxis);
            focus.select(".axis--y").call(yAxis);
            
            const newCandleW = Math.max(2, (width / visibleData.length) * 0.6);
            
            focusChart.selectAll(".stem")
                .attr("x1", d => x(d.date)).attr("x2", d => x(d.date))
                .attr("y1", d => y(d.high)).attr("y2", d => y(d.low));
                
            focusChart.selectAll(".body")
                .attr("x", d => x(d.date) - newCandleW/2).attr("width", newCandleW)
                .attr("y", d => y(Math.max(d.open, d.close)))
                .attr("height", d => Math.max(2, Math.abs(y(d.open) - y(d.close))));
        }
        // 新增：在页面中动态创建一个隐藏的 Tooltip 框
        d3.select(".d3-tooltip").remove(); // 防止重复创建
        const tooltip = d3.select("body").append("div")
            .attr("class", "d3-tooltip")
            .style("position", "absolute")
            .style("background", "rgba(0, 0, 0, 0.85)") // 半透明黑色背景
            .style("color", "#fff")
            .style("padding", "10px")
            .style("border-radius", "5px")
            .style("font-size", "12px")
            .style("pointer-events", "none") // 防止鼠标闪烁
            .style("opacity", 0)
            .style("z-index", 1000);
    }

    // --- VIS 3: STREAMGRAPH (高对比度核心) ---
    function renderVis3(data) {
        const el = document.getElementById('vis3-main');
        const w = el.clientWidth - margin.left - margin.right;
        const h = el.clientHeight - margin.top - margin.bottom;

        const keys = ["hype", "fear", "anger"];
        const stack = d3.stack().keys(keys).offset(d3.stackOffsetNone);
        const layers = stack(data);

        const svg = d3.select("#vis3-main").append("svg").attr("width", w + margin.left + margin.right).attr("height", h + margin.top + margin.bottom)
            .append("g").attr("transform", `translate(${margin.left},${margin.top})`);

        const x = d3.scaleTime().domain(d3.extent(data, d => d.date)).range([0, w]);
        const y = d3.scaleLinear().domain([0, d3.max(layers, l => d3.max(l, d => d[1]))]).range([h, 0]);

        const area = d3.area().x(d => x(d.data.date)).y0(d => y(d[0])).y1(d => y(d[1])).curve(d3.curveBasis);

        svg.selectAll("path").data(layers).enter().append("path")
            .attr("d", area).attr("fill", d => getSentColor(d.key)).attr("opacity", 0.9)
            .on("mousemove", (event) => {
                const date = x.invert(d3.pointer(event)[0]);
                updateComments(date);
            });
        // 修复重叠的 X 轴并倾斜文字
        svg.append("g")
            .attr("transform", `translate(0,${h})`)
            .attr("class", "axis")
            .call(d3.axisBottom(x).tickFormat(d3.timeFormat("%b %d")))
            .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", "rotate(-45)");

        // 补全缺失的 Y 轴和标题
        svg.append("g").attr("class", "axis").call(d3.axisLeft(y).ticks(5));
        svg.append("text")
            .attr("transform", "rotate(-90)").attr("y", 0 - margin.left).attr("x", 0 - (h / 2))
            .attr("dy", "1em").style("text-anchor", "middle").style("font-size", "12px").text("Total Reddit Posts");
        const hoverLine = svg.append("line")
            .attr("class", "hover-line").attr("y1", 0).attr("y2", h)
            .style("stroke", "#1a1a1a").style("stroke-width", "1.5px").style("stroke-dasharray", "4,4").style("opacity", 0);

        d3.select(".vis3-tooltip").remove();
        const tooltip3 = d3.select("body").append("div").attr("class", "vis3-tooltip")
            .style("position", "absolute").style("background", "rgba(255, 255, 255, 0.95)")
            .style("color", "#333").style("padding", "12px").style("border", "1px solid #dee2e6")
            .style("border-radius", "8px").style("font-size", "13px")
            .style("box-shadow", "0 4px 12px rgba(0,0,0,0.1)")
            .style("pointer-events", "none").style("opacity", 0).style("z-index", 1000);

        const bisectDate = d3.bisector(d => d.date).left;

        svg.append("rect").attr("width", w).attr("height", h)
            .style("fill", "none").style("pointer-events", "all")
            .on("mouseover", () => { hoverLine.style("opacity", 1); tooltip3.style("opacity", 1); })
            .on("mouseout", () => { hoverLine.style("opacity", 0); tooltip3.style("opacity", 0); })
            .on("mousemove", function(event) {
                const mouseX = d3.pointer(event)[0];
                const x0 = x.invert(mouseX);
                const i = bisectDate(data, x0, 1);
                const d0 = data[i - 1], d1 = data[i];
                if (!d0 || !d1) return;
                const d = (x0 - d0.date > d1.date - x0) ? d1 : d0; 

                const exactX = x(d.date);
                hoverLine.attr("x1", exactX).attr("x2", exactX); 
                updateComments(d.date); 

                const total = d.hype + d.fear + d.anger;

                tooltip3.html(`
                    <div style="margin-bottom:8px; border-bottom:1px solid #dee2e6; padding-bottom:5px; font-weight:bold; font-size:14px;">
                        ${d3.timeFormat("%b %d, %Y")(d.date)}
                    </div>
                    <div style="display:flex; justify-content:space-between; width:150px;">
                        <span><span style="color:${palette.Hype}; font-size:16px;">■</span> Hype:</span> <b>${d.hype}</b>
                    </div>
                    <div style="display:flex; justify-content:space-between; width:150px;">
                        <span><span style="color:${palette.Fear}; font-size:16px;">■</span> Fear:</span> <b>${d.fear}</b>
                    </div>
                    <div style="display:flex; justify-content:space-between; width:150px;">
                        <span><span style="color:${palette.Anger}; font-size:16px;">■</span> Anger:</span> <b>${d.anger}</b>
                    </div>
                    <div style="margin-top:8px; padding-top:5px; border-top:1px dashed #dee2e6; display:flex; justify-content:space-between; width:150px;">
                        <span style="color:#6c757d;">Total Posts:</span> <b>${total}</b>
                    </div>
                `)
                .style("left", (event.pageX + 20) + "px")
                .style("top", (event.pageY - 60) + "px");
            });

    }

    // --- 🎬 VIS 5: ALIGNER  ---
    function renderVis5(data) {
        const el = document.getElementById('vis5');
        const w = el.clientWidth - margin.left - margin.right;
        const h = el.clientHeight - margin.top - margin.bottom;

        //清空旧画布，防止拖动窗口时图表重叠
        d3.select("#vis5").selectAll("*").remove();

        const svg = d3.select("#vis5").append("svg").attr("width", w + margin.left + margin.right).attr("height", h + margin.top + margin.bottom)
            .append("g").attr("transform", `translate(${margin.left},${margin.top})`);

        //创建剪裁蒙版，防止红线拖出图表外
        svg.append("defs").append("clipPath").attr("id", "clip-vis5")
            .append("rect").attr("width", w).attr("height", h);

        const x = d3.scaleTime().domain(d3.extent(data, d => d.date)).range([0, w]);
        const yL = d3.scaleLinear().domain([0, d3.max(data, d => d.fear)]).range([h, 0]);
        const yR = d3.scaleLinear().domain([0, d3.max(data, d => d.volatility)]).range([h, 0]);

        // 波动率：作为背景面积图
        svg.append("path").datum(data).attr("fill", palette.VolLine).attr("opacity", 0.5)
            .attr("d", d3.area().x(d => x(d.date)).y0(h).y1(d => yR(d.volatility)).curve(d3.curveMonotoneX));

        // 定义 lineGroup 并套上剪裁蒙版
        const lineGroup = svg.append("g").attr("clip-path", "url(#clip-vis5)");
        // 情绪线：鲜艳的红色 (使用 d.fear)
        const fearPath = lineGroup.append("path").datum(data)
            .attr("fill", "none").attr("stroke", palette.Anger).attr("stroke-width", 3)
            .attr("d", d3.line().x(d => x(d.date)).y(d => yL(d.fear)).curve(d3.curveMonotoneX));
        
        svg.append("g").attr("transform", `translate(0,${h})`).attr("class", "axis")
            .call(d3.axisBottom(x).tickFormat(d3.timeFormat("%b %d")))
            .selectAll("text").style("text-anchor", "end").attr("dx", "-.8em").attr("dy", ".15em").attr("transform", "rotate(-45)");
            
        svg.append("g").attr("class", "axis").attr("color", palette.Anger).call(d3.axisLeft(yL).ticks(5));
        svg.append("text").attr("transform", "rotate(-90)").attr("y", -margin.left + 15).attr("x", -(h / 2))
            .style("text-anchor", "middle").style("fill", palette.Anger).style("font-weight", "bold").style("font-size", "12px").text("Fear Posts Volume");

        svg.append("g").attr("transform", `translate(${w},0)`).attr("class", "axis").attr("color", "#6c757d").call(d3.axisRight(yR).ticks(5));
        svg.append("text").attr("transform", "rotate(-90)").attr("y", w + margin.right - 15).attr("x", -(h / 2))
            .style("text-anchor", "middle").style("fill", "#6c757d").style("font-weight", "bold").style("font-size", "12px").text("Market Volatility");

        /// 拖动交互 (修复日历时间差 Bug)
        const oneDayMs = 24 * 60 * 60 * 1000; // 一天有多少毫秒
        const minDate = x.domain()[0]; // 拿到第一天
        // 核心：用 D3 直接算出来，“真实的一天”在屏幕上到底占多少个像素
        const pixelPerDay = x(new Date(minDate.getTime() + oneDayMs)) - x(minDate);

        d3.select("#shiftSlider").on("input", function() {
            const v = +this.value;
            d3.select("#shiftLabel").text(v > 0 ? `+${v} Days` : (v === 0 ? "0 Days" : `${v} Days`));
            fearPath.attr("transform", `translate(${v * pixelPerDay}, 0)`);
        });
    }

})();