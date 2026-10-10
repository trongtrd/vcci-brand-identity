# Sample charts with the VCCI ggplot2 theme:  Rscript charts.R OUTDIR [CHARTS_DIR]
# Writes r-<chart>.svg for the chart checks in run_tests.py (layer 8). The same charts are drawn in Python and Stata.
args <- commandArgs(trailingOnly = TRUE)
out <- normalizePath(args[1], winslash = "/")
here <- dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)), winslash = "/"))
charts_dir <- if (length(args) > 1) args[2] else file.path(here, "..", "..", "charts")
suppressPackageStartupMessages(library(ggplot2))
source(file.path(charts_dir, "theme_vcci.R"), encoding = "UTF-8")
setwd(out)   # fonts are looked up from here (the extension's fonts, or the brand system's)
vcci_setup("vi")

data <- function(n) read.csv(file.path(here, "data", paste0(n, ".csv")), encoding = "UTF-8", fileEncoding = "UTF-8")
src <- "Nguồn: VCCI · Số liệu minh họa"
save <- function(p, name, height = 3.6) ggsave(file.path(out, paste0("r-", name, ".svg")), p, width = 6.5, height = height,
                                               device = svglite::svglite)

# column chart, one value highlighted in gold with its label
d <- data("bar")
p <- ggplot(d, aes(factor(year), score, fill = vcci_highlight(year == 2025))) +
  geom_col(width = 0.62) + scale_fill_identity() +
  geom_text(data = subset(d, year == 2025), aes(label = label_vcci(accuracy = 0.1)(score)), vjust = -0.6) +
  scale_y_continuous(limits = c(0, 80), breaks = seq(0, 80, 10), expand = c(0, 0)) +
  labs(x = NULL, y = NULL, title = "Năm 2025 đạt điểm cao nhất trong sáu năm", caption = src)
save(p, "bar")

# three lines, named at their ends
d <- data("line")
d$city <- factor(d$city, levels = unique(d$city))
ends <- d[d$year == max(d$year), ]
p <- ggplot(d, aes(year, score, colour = city)) + geom_line() +
  geom_text(data = ends, aes(label = city), hjust = 0, nudge_x = 0.08, family = vcci_font$text, fontface = "bold", size = 8 / .pt) +
  scale_colour_vcci(guide = "none") +
  scale_x_continuous(breaks = 2020:2025, expand = expansion(add = c(0.2, 0.8))) +
  scale_y_continuous(limits = c(55, 75), breaks = seq(55, 75, 2.5)) +
  labs(x = NULL, y = NULL, title = "Hà Nội vượt TP.HCM và Đà Nẵng từ năm 2024", caption = src)
save(p, "line")

# stacked horizontal bars (shares), percentages on the segments
d <- data("stack")
d$rating <- factor(d$rating, levels = unique(d$rating[order(d$order)]))
d$group <- factor(d$group, levels = rev(unique(d$group)))
p <- ggplot(d, aes(share, group, fill = rating)) + geom_col(width = 0.55, position = position_stack(reverse = TRUE)) +
  geom_text(aes(label = paste0(share, "%"), colour = rating), position = position_stack(vjust = 0.5, reverse = TRUE),
            family = vcci_font$text, fontface = "bold", size = 7.5 / .pt, show.legend = FALSE) +
  scale_fill_vcci() + scale_colour_manual(values = c("white", vcci_colours[["Ink"]], "white", "white")) +
  scale_x_continuous(expand = c(0, 0)) +
  labs(x = NULL, y = NULL, title = "Doanh nghiệp nhỏ đánh giá tích cực hơn", caption = src) +
  theme(axis.text.x = element_blank(), axis.line.x = element_blank(), axis.ticks.x = element_blank(),
        panel.grid.major.y = element_blank())
save(p, "stack", height = 2.6)

# scatter, two groups
d <- data("scatter")
d$sector <- factor(d$sector, levels = unique(d$sector))
p <- ggplot(d, aes(employees, cost, colour = sector)) + geom_point(size = 1.6) +
  scale_y_continuous(limits = c(0, NA)) +
  labs(x = "Số lao động", y = "Chi phí không chính thức (% doanh thu)", title = "Chi phí không chính thức tăng theo quy mô", caption = src)
save(p, "scatter")

# six series: the full series order
d <- data("series6")
d$sector <- factor(d$sector, levels = unique(d$sector[order(d$order)]))
ends <- d[d$year == max(d$year), ]
p <- ggplot(d, aes(year, value, colour = sector)) + geom_line() +
  geom_text(data = ends, aes(label = sector), hjust = 0, nudge_x = 0.08, family = vcci_font$text, fontface = "bold", size = 8 / .pt) +
  scale_colour_vcci(guide = "none") +
  scale_x_continuous(breaks = 2020:2025, expand = expansion(add = c(0.2, 0.9))) +
  labs(x = NULL, y = NULL, title = "Sáu ngành theo thứ tự màu chuỗi", caption = src)
save(p, "series6")

# heat map, seven ordered classes (light = low)
d <- data("heat")
d$region <- factor(d$region, levels = rev(unique(d$region[order(d$order)])))
d$class <- cut(d$score, breaks = 59 + 1.5 * 0:7, include.lowest = TRUE)
p <- ggplot(d, aes(factor(year), region, fill = class)) + geom_tile(colour = "white", linewidth = 1.5 / .pt) +
  geom_text(aes(label = label_vcci(accuracy = 0.1)(score), colour = score >= 65), family = vcci_font$text, size = 7.5 / .pt) +
  scale_fill_vcci_seq(drop = FALSE, guide = "none") +
  scale_colour_manual(values = c(`FALSE` = vcci_colours[["Ink"]], `TRUE` = "white"), guide = "none") +
  scale_x_discrete(expand = c(0, 0)) + scale_y_discrete(expand = c(0, 0)) +
  labs(x = NULL, y = NULL, title = "Đông Nam Bộ dẫn đầu, Tây Nguyên cải thiện nhanh", caption = src) +
  theme(axis.line.x = element_blank(), axis.ticks.x = element_blank(), panel.grid.major.y = element_blank())
save(p, "heat")
cat("R charts ->", out, "\n")
