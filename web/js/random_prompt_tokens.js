import { app } from "../../../scripts/app.js";

const NODE_NAME = "RandomPromptTokens";
const MAIN_LINES = 20;
const OPTION_LINES = 5;
const LINE_HEIGHT = 18;
const WIDGET_PADDING = 16;

function sizeTextWidget(widget, lines, allowResize) {
    if (!widget) return;

    const height = lines * LINE_HEIGHT + WIDGET_PADDING;
    widget.options ??= {};
    widget.options.lines = lines;

    if (!widget.__randomPromptComputeSizeInstalled) {
        widget.__randomPromptOriginalComputeSize =
            typeof widget.computeSize === "function"
                ? widget.computeSize.bind(widget)
                : null;
        widget.computeSize = function (width) {
            const base = this.__randomPromptOriginalComputeSize
                ? this.__randomPromptOriginalComputeSize(width)
                : [width, 0];
            const resizedHeight = this.__randomPromptResizedHeight || 0;
            return [base[0], Math.max(base[1], height, resizedHeight)];
        };
        widget.__randomPromptComputeSizeInstalled = true;
    }

    const input = widget.inputEl;
    if (!input) return;

    const container = input.parentElement;
    const rowHeight = widget.__randomPromptResizedHeight || height;
    if (container) {
        container.style.height = `${rowHeight}px`;
        container.style.minHeight = `${rowHeight}px`;
        container.style.overflow = "visible";
    }

    input.rows = lines;
    input.style.boxSizing = "border-box";
    input.style.height = `${height}px`;
    input.style.minHeight = `${height}px`;
    input.style.overflowY = "auto";
    input.style.resize = allowResize ? "vertical" : "none";
    if (!allowResize) input.style.maxHeight = `${height}px`;
    input.style.border = "1px solid rgba(255, 255, 255, 0.18)";
    input.style.borderRadius = "4px";
    input.style.padding = "6px 8px";
    input.style.background = "rgba(0, 0, 0, 0.2)";
    input.style.display = "";

    if (allowResize && !widget.__randomPromptResizeObserver && typeof ResizeObserver !== "undefined") {
        widget.__randomPromptResizeObserver = new ResizeObserver(() => {
            const resizedHeight = input.offsetHeight;
            if (resizedHeight <= 0) return;
            widget.__randomPromptResizedHeight = resizedHeight;
            if (container) {
                container.style.height = `${resizedHeight}px`;
                container.style.minHeight = `${resizedHeight}px`;
            }
            const node = widget.__randomPromptNode;
            const size = node?.computeSize?.();
            if (size) {
                size[0] = Math.max(size[0], 420);
                node.setSize?.(size);
                node.setDirtyCanvas?.(true, true);
            }
        });
        widget.__randomPromptResizeObserver.observe(input);
    }
}

function applySizing(node) {
    if (!node?.widgets) return;

    const main = node.widgets.find((widget) => widget.name === "text");
    for (const widget of node.widgets) {
        widget.__randomPromptNode = node;
    }
    sizeTextWidget(main, MAIN_LINES, true);

    for (const widget of node.widgets) {
        if (/^options_\d{3}$/.test(widget.name)) {
            sizeTextWidget(widget, OPTION_LINES, false);
        }
    }

    const size = node.computeSize?.();
    if (size) {
        size[0] = Math.max(size[0], 420);
        node.setSize?.(size);
    }
    node.setDirtyCanvas?.(true, true);
}

app.registerExtension({
    name: "ComfyUI.RandomPromptTokens.widgetSizing",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData?.name !== NODE_NAME) return;

        const originalOnNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            const result = originalOnNodeCreated?.apply(this, arguments);
            requestAnimationFrame(() => applySizing(this));
            return result;
        };

        const originalOnConfigure = nodeType.prototype.onConfigure;
        nodeType.prototype.onConfigure = function () {
            const result = originalOnConfigure?.apply(this, arguments);
            requestAnimationFrame(() => applySizing(this));
            return result;
        };
    },
});
