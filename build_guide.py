import os
import subprocess
import pypdf

# Python script to generate high-quality HTML and PDF for the gRPC Beginner Guide

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>gRPC Made Simple: Distributed Systems Beginner Guide</title>
<style>
  @page {
    size: A4 portrait;
    margin: 0;
  }
  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: #f8fafc;
    color: #1e293b;
  }
  .page {
    width: 210mm;
    height: 297mm;
    max-height: 297mm;
    padding: 16mm 18mm 14mm 18mm;
    margin: 0 auto 10mm auto;
    background: #ffffff;
    position: relative;
    page-break-after: always;
    page-break-inside: avoid;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
  }
  @media print {
    body { background: transparent; }
    .page {
      margin: 0;
      box-shadow: none;
      page-break-after: always;
      page-break-inside: avoid;
    }
  }

  /* Header & Section Tags */
  .header-tag {
    display: inline-block;
    font-size: 11pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #2563eb;
    background: #eff6ff;
    padding: 3px 10px;
    border-radius: 6px;
    margin-bottom: 6px;
  }
  h1.page-title {
    font-size: 26pt;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 4px 0;
    line-height: 1.15;
  }
  h2.page-subtitle {
    font-size: 15pt;
    font-weight: 500;
    color: #64748b;
    margin: 0 0 12px 0;
    line-height: 1.3;
  }

  /* Body Content */
  .page-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }
  p {
    font-size: 15.5pt;
    line-height: 1.45;
    color: #334155;
    margin: 0 0 10px 0;
  }
  p strong {
    color: #0f172a;
  }
  ul {
    margin: 4px 0 10px 20px;
    padding: 0;
  }
  li {
    font-size: 15pt;
    line-height: 1.4;
    color: #334155;
    margin-bottom: 6px;
  }

  /* Callout Boxes */
  .callout {
    border-radius: 8px;
    padding: 10px 14px;
    margin: 10px 0;
    font-size: 14pt;
    line-height: 1.4;
  }
  .callout-title {
    font-weight: 700;
    font-size: 14pt;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .callout-body {
    margin: 0;
  }
  .callout-blue {
    background-color: #eff6ff;
    border-left: 5px solid #2563eb;
  }
  .callout-blue .callout-title { color: #1d4ed8; }
  .callout-blue .callout-body { color: #1e40af; }

  .callout-green {
    background-color: #f0fdf4;
    border-left: 5px solid #16a34a;
  }
  .callout-green .callout-title { color: #15803d; }
  .callout-green .callout-body { color: #166534; }

  .callout-red {
    background-color: #fef2f2;
    border-left: 5px solid #dc2626;
  }
  .callout-red .callout-title { color: #b91c1c; }
  .callout-red .callout-body { color: #991b1b; }

  .callout-amber {
    background-color: #fffbeb;
    border-left: 5px solid #d97706;
  }
  .callout-amber .callout-title { color: #b45309; }
  .callout-amber .callout-body { color: #92400e; }

  /* Code Block */
  pre.code-block {
    background: #0f172a;
    color: #f8fafc;
    padding: 11px 14px;
    border-radius: 8px;
    font-family: "Consolas", "Fira Code", monospace;
    font-size: 12.5pt;
    line-height: 1.35;
    margin: 8px 0;
    overflow: hidden;
    border: 1px solid #334155;
  }
  .code-kw { color: #f43f5e; font-weight: 600; }
  .code-fn { color: #38bdf8; }
  .code-str { color: #a3e635; }
  .code-cm { color: #94a3b8; font-style: italic; }
  .code-num { color: #fbbf24; }

  /* Footer */
  .page-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #e2e8f0;
    padding-top: 8px;
    font-size: 11pt;
    color: #94a3b8;
    margin-top: 6px;
  }
  .footer-left { font-weight: 600; color: #64748b; }
  .footer-right { font-weight: 700; color: #2563eb; }

  /* Title Page Custom */
  .title-page-container {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
    padding: 25mm 0 15mm 0;
  }
  .title-badge {
    background: #e0e7ff;
    color: #4338ca;
    font-size: 13pt;
    font-weight: 700;
    padding: 6px 16px;
    border-radius: 9999px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .main-heading {
    font-size: 38pt;
    font-weight: 900;
    color: #0f172a;
    line-height: 1.15;
    margin: 15px 0 10px 0;
  }
  .main-subheading {
    font-size: 19pt;
    color: #475569;
    max-width: 600px;
    line-height: 1.35;
  }
  .title-meta {
    font-size: 13pt;
    color: #64748b;
    line-height: 1.6;
  }

  /* Table styling */
  table.simple-table {
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0;
    font-size: 13pt;
  }
  table.simple-table th {
    background: #f1f5f9;
    color: #0f172a;
    text-align: left;
    padding: 8px 10px;
    font-weight: 700;
    border-bottom: 2px solid #cbd5e1;
  }
  table.simple-table td {
    padding: 8px 10px;
    border-bottom: 1px solid #e2e8f0;
    color: #334155;
    line-height: 1.35;
  }
</style>
</head>
<body>

<!-- PAGE 1: TITLE PAGE -->
<div class="page">
  <div class="title-page-container">
    <div>
      <span class="title-badge">Distributed Systems · Practical Guide</span>
      <h1 class="main-heading">gRPC Made Simple</h1>
      <p class="main-subheading">A Beginner's Walkthrough to Building a Distributed Restaurant System from Scratch</p>
    </div>

    <!-- Title Vector Illustration -->
    <div style="margin: 20px 0;">
      <svg width="420" height="230" viewBox="0 0 520 280">
        <defs>
          <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#10b981"/>
          </marker>
        </defs>
        <rect x="10" y="10" width="500" height="260" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
        <!-- Kitchen Box -->
        <rect x="200" y="30" width="120" height="90" rx="10" fill="#eff6ff" stroke="#3b82f6" stroke-width="2.5"/>
        <text x="260" y="65" font-size="28" text-anchor="middle">🍳</text>
        <text x="260" y="92" font-size="14" font-weight="bold" fill="#1d4ed8" text-anchor="middle">KITCHEN</text>
        <text x="260" y="108" font-size="11" fill="#64748b" text-anchor="middle">(gRPC Server)</text>
        <!-- Customer Box -->
        <rect x="40" y="150" width="130" height="90" rx="10" fill="#ecfdf5" stroke="#10b981" stroke-width="2.5"/>
        <text x="105" y="185" font-size="28" text-anchor="middle">👤</text>
        <text x="105" y="212" font-size="14" font-weight="bold" fill="#047857" text-anchor="middle">CUSTOMER</text>
        <text x="105" y="228" font-size="11" fill="#64748b" text-anchor="middle">(Cliente Console)</text>
        <!-- Driver Box -->
        <rect x="350" y="150" width="130" height="90" rx="10" fill="#fffbeb" stroke="#f59e0b" stroke-width="2.5"/>
        <text x="415" y="185" font-size="28" text-anchor="middle">🛵</text>
        <text x="415" y="212" font-size="14" font-weight="bold" fill="#b45309" text-anchor="middle">COURIER</text>
        <text x="415" y="228" font-size="11" fill="#64748b" text-anchor="middle">(Repartidor App)</text>
        <!-- Connectors -->
        <path d="M 120 150 L 220 110" stroke="#10b981" stroke-width="2.5" stroke-dasharray="6,4" fill="none" marker-end="url(#arrow-green)"/>
        <path d="M 300 110 L 390 150" stroke="#f59e0b" stroke-width="2.5" stroke-dasharray="6,4" fill="none"/>
        <rect x="210" y="180" width="100" height="40" rx="6" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="1.5"/>
        <text x="260" y="200" font-size="11" font-weight="bold" fill="#6d28d9" text-anchor="middle">HTTP/2 Network</text>
        <text x="260" y="214" font-size="9" fill="#7c3aed" text-anchor="middle">Port 5000</text>
      </svg>
    </div>

    <div class="title-meta">
      <p style="margin: 0; font-weight: 700; color: #1e293b;">Based on Distributed Systems Lab 2 (UCLM)</p>
      <p style="margin: 4px 0 0 0; color: #64748b;">Step-by-Step Practical Companion · C# & .NET 8</p>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">gRPC Made Simple</span>
    <span class="footer-right">Page 1</span>
  </div>
</div>

<!-- PAGE 2: TABLE OF CONTENTS & LEGEND -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Overview</span>
    <h1 class="page-title">Table of Contents</h1>
    <h2 class="page-subtitle">Your roadmap to gRPC mastery</h2>

    <table class="simple-table" style="margin-bottom: 10px;">
      <tr><th style="width: 15%;">Sec</th><th>Topic</th><th style="width: 15%; text-align: right;">Page</th></tr>
      <tr><td><b>1</b></td><td>Title & Table of Contents</td><td style="text-align: right;">1 – 2</td></tr>
      <tr><td><b>2</b></td><td>The Big Picture & Restaurant Analogy</td><td style="text-align: right;">3 – 4</td></tr>
      <tr><td><b>3</b></td><td>Why gRPC? The REST/JSON Problem</td><td style="text-align: right;">5</td></tr>
      <tr><td><b>4</b></td><td>How Pieces Talk & RPC Flow</td><td style="text-align: right;">6 – 7</td></tr>
      <tr><td><b>5</b></td><td>The .proto File Line by Line</td><td style="text-align: right;">8 – 9</td></tr>
      <tr><td><b>6</b></td><td>Code Generation (protoc)</td><td style="text-align: right;">10</td></tr>
      <tr><td><b>7</b></td><td>The Lab Step by Step</td><td style="text-align: right;">11 – 21</td></tr>
      <tr><td><b>8</b></td><td>Common Mistakes & Fixes</td><td style="text-align: right;">22</td></tr>
      <tr><td><b>9</b></td><td>Cheat Sheet & 5 Quiz Questions</td><td style="text-align: right;">23 – 24</td></tr>
    </table>

    <div class="callout callout-blue" style="padding: 6px 12px; margin: 4px 0;">
      <div class="callout-title" style="margin: 0;">💡 Blue Box: Why?</div>
      <div class="callout-body">Explains engineering reasons behind choices.</div>
    </div>
    <div class="callout callout-green" style="padding: 6px 12px; margin: 4px 0;">
      <div class="callout-title" style="margin: 0;">📌 Green Box: Remember</div>
      <div class="callout-body">Key rules to keep programs running smoothly.</div>
    </div>
    <div class="callout callout-red" style="padding: 6px 12px; margin: 4px 0;">
      <div class="callout-title" style="margin: 0;">⚠️ Red Box: Warning</div>
      <div class="callout-body">Common stumbling blocks causing runtime errors.</div>
    </div>
    <div class="callout callout-amber" style="padding: 6px 12px; margin: 4px 0;">
      <div class="callout-title" style="margin: 0;">📝 Amber Box: Notes</div>
      <div class="callout-body">Clarifies missing or unclear lab details.</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Overview · Table of Contents</span>
    <span class="footer-right">Page 2</span>
  </div>
</div>

<!-- PAGE 3: THE BIG PICTURE - WHAT WE BUILD -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Section 2 · The Big Picture</span>
    <h1 class="page-title">What We Build</h1>
    <h2 class="page-subtitle">A distributed restaurant across three independent programs</h2>

    <p>Welcome! We are building an online order system for <strong>"Distributed Systems and Fun"</strong>.</p>
    <p>We build <strong>three console programs</strong>:</p>

    <ul>
      <li><strong>Restaurante (Kitchen)</strong>: Central gRPC server with a thread-safe order queue.</li>
      <li><strong>Cliente (Customer)</strong>: Places orders and queries status.</li>
      <li><strong>Repartidor (Courier)</strong>: Waits for ready food and delivers it.</li>
    </ul>

    <p>You will run all three in separate terminals and watch them interact in real time!</p>

    <div class="callout callout-blue">
      <div class="callout-title">💡 Why separate programs?</div>
      <div class="callout-body">In real systems, customers, kitchens, and drivers run on different machines and must communicate reliably.</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Section 2 · The Big Picture</span>
    <span class="footer-right">Page 3</span>
  </div>
</div>

<!-- PAGE 4: THE RESTAURANT ANALOGY & ARCHITECTURE -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Section 2 · Architecture & Analogy</span>
    <h1 class="page-title">The Restaurant Analogy</h1>
    <h2 class="page-subtitle">Mapping real restaurant roles directly to gRPC components</h2>

    <p>To make distributed systems easy to understand, we use <strong>one single analogy</strong> throughout this guide:</p>

    <!-- Diagram 5 & 1: Restaurant Analogy Architecture -->
    <div style="margin: 6px 0 10px 0; text-align: center;">
      <svg width="490" height="230" viewBox="0 0 540 250">
        <rect x="5" y="5" width="530" height="240" rx="14" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
        <!-- Customer -->
        <rect x="25" y="25" width="145" height="185" rx="10" fill="#ecfdf5" stroke="#10b981" stroke-width="2"/>
        <text x="97" y="60" font-size="30" text-anchor="middle">👤</text>
        <text x="97" y="88" font-size="14" font-weight="bold" fill="#065f46" text-anchor="middle">CUSTOMER</text>
        <text x="97" y="108" font-size="12" font-weight="bold" fill="#047857" text-anchor="middle">= gRPC Client</text>
        <text x="97" y="132" font-size="11" fill="#475569" text-anchor="middle">Decides what to eat</text>
        <text x="97" y="150" font-size="11" fill="#475569" text-anchor="middle">Hands ticket to waiter</text>
        <rect x="35" y="165" width="125" height="32" rx="6" fill="#ffffff" stroke="#10b981"/>
        <text x="97" y="185" font-size="11" font-weight="bold" fill="#047857" text-anchor="middle">Cliente Program</text>

        <!-- Waiter / Stub & Network -->
        <rect x="195" y="25" width="150" height="185" rx="10" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="2"/>
        <text x="270" y="60" font-size="30" text-anchor="middle">📋</text>
        <text x="270" y="88" font-size="14" font-weight="bold" fill="#5b21b6" text-anchor="middle">MENU & WAITER</text>
        <text x="270" y="108" font-size="12" font-weight="bold" fill="#6d28d9" text-anchor="middle">= Proto & Stub</text>
        <text x="270" y="132" font-size="11" fill="#475569" text-anchor="middle">Menu: .proto contract</text>
        <text x="270" y="150" font-size="11" fill="#475569" text-anchor="middle">Waiter: Stub helper</text>
        <rect x="205" y="165" width="130" height="32" rx="6" fill="#ffffff" stroke="#8b5cf6"/>
        <text x="270" y="185" font-size="11" font-weight="bold" fill="#6d28d9" text-anchor="middle">HTTP/2 Tube (Port 5000)</text>

        <!-- Kitchen -->
        <rect x="370" y="25" width="145" height="185" rx="10" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
        <text x="442" y="60" font-size="30" text-anchor="middle">👨‍🍳</text>
        <text x="442" y="88" font-size="14" font-weight="bold" fill="#1e40af" text-anchor="middle">KITCHEN</text>
        <text x="442" y="108" font-size="12" font-weight="bold" fill="#1d4ed8" text-anchor="middle">= gRPC Server</text>
        <text x="442" y="132" font-size="11" fill="#475569" text-anchor="middle">Cooks food in FIFO order</text>
        <text x="442" y="150" font-size="11" fill="#475569" text-anchor="middle">Rings bell when ready</text>
        <rect x="380" y="165" width="125" height="32" rx="6" fill="#ffffff" stroke="#3b82f6"/>
        <text x="442" y="185" font-size="11" font-weight="bold" fill="#1d4ed8" text-anchor="middle">Restaurante Program</text>
      </svg>
    </div>

    <div class="callout callout-green">
      <div class="callout-title">📌 Remember</div>
      <div class="callout-body">Each program runs in its own console window without sharing memory. All data moves over HTTP/2 using binary Protocol Buffers.</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Section 2 · Architecture & Analogy</span>
    <span class="footer-right">Page 4</span>
  </div>
</div>

<!-- PAGE 5: WHY gRPC? -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Section 3 · Why gRPC?</span>
    <h1 class="page-title">The Problem It Solves</h1>
    <h2 class="page-subtitle">Moving beyond slow, verbose REST and JSON</h2>

    <p>Traditional APIs use <strong>REST</strong> with <strong>JSON text</strong>. While readable, JSON has big drawbacks:</p>

    <ul>
      <li><strong>Bulky Text</strong>: Repeating keys like <code>"id_pedido"</code> wastes bandwidth.</li>
      <li><strong>Slow Parsing</strong>: Parsing numbers from text burns CPU cycles.</li>
      <li><strong>No Strict Contract</strong>: Typos cause silent runtime crashes!</li>
    </ul>

    <p><strong>Restaurant Analogy:</strong> REST is mailing a long letter to order soup. gRPC is sending a numbered ticket through a pneumatic tube: instant, tiny, and foolproof.</p>

    <div class="callout callout-blue">
      <div class="callout-title">💡 Why is gRPC faster?</div>
      <div class="callout-body">gRPC encodes messages in binary Protocol Buffers: up to 7x smaller and 8x faster than JSON!</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Section 3 · Why gRPC?</span>
    <span class="footer-right">Page 5</span>
  </div>
</div>

<!-- PAGE 6: HOW THE PIECES TALK -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Section 4 · How the Pieces Talk</span>
    <h1 class="page-title">The Five Key Players</h1>
    <h2 class="page-subtitle">How client, server, stub, HTTP/2, and protobuf work together</h2>

    <p>Meet the five components that make gRPC communication work seamlessly:</p>

    <ul>
      <li><strong>Client</strong>: The app requesting work (the customer).</li>
      <li><strong>Server</strong>: The central app doing the work (the kitchen).</li>
      <li><strong>Client Stub (Proxy)</strong>: A generated local helper class that makes remote calls feel like local C# methods.</li>
      <li><strong>Protocol Buffers</strong>: Google's compact binary format for encoding data.</li>
      <li><strong>HTTP/2</strong>: Modern transport protocol that multiplexes many requests over one connection.</li>
    </ul>

    <div class="callout callout-green">
      <div class="callout-title">📌 Remember: Network Transparency</div>
      <div class="callout-body">Network transparency lets you write <code>await client.HacerPedidoAsync()</code> without writing raw network socket code!</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Section 4 · How the Pieces Talk</span>
    <span class="footer-right">Page 6</span>
  </div>
</div>

<!-- PAGE 7: REQUEST / RESPONSE FLOW (DIAGRAM 2) -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Section 4 · Communication Flow</span>
    <h1 class="page-title">Request & Response Flow</h1>
    <h2 class="page-subtitle">Tracing an RPC call from C# method to binary bytes and back</h2>

    <!-- Diagram 2: Detailed Flow with labeled arrows -->
    <div style="margin: 4px 0 10px 0; text-align: center;">
      <svg width="490" height="260" viewBox="0 0 540 270">
        <defs>
          <marker id="arrow-flow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#3b82f6"/>
          </marker>
        </defs>
        <rect x="5" y="5" width="530" height="260" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
        
        <!-- Left Column: Client -->
        <rect x="20" y="20" width="150" height="60" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="2"/>
        <text x="95" y="45" font-size="12" font-weight="bold" fill="#065f46" text-anchor="middle">1. Client Code</text>
        <text x="95" y="65" font-size="11" fill="#047857" text-anchor="middle">Calls HacerPedidoAsync()</text>

        <rect x="20" y="105" width="150" height="60" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
        <text x="95" y="130" font-size="12" font-weight="bold" fill="#1e40af" text-anchor="middle">2. Client Stub</text>
        <text x="95" y="150" font-size="11" fill="#1d4ed8" text-anchor="middle">Serializes to Protobuf</text>

        <!-- Middle: Network -->
        <rect x="205" y="65" width="130" height="140" rx="8" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="2"/>
        <text x="270" y="95" font-size="13" font-weight="bold" fill="#5b21b6" text-anchor="middle">3. HTTP/2</text>
        <text x="270" y="115" font-size="10" fill="#6d28d9" text-anchor="middle">Binary Stream</text>
        <text x="270" y="135" font-size="18" text-anchor="middle">⚡ 010110 ⚡</text>
        <text x="270" y="160" font-size="10" fill="#6d28d9" text-anchor="middle">TCP Port 5000</text>
        <text x="270" y="180" font-size="10" fill="#7c3aed" text-anchor="middle">Multiplexed</text>

        <!-- Right Column: Server -->
        <rect x="370" y="105" width="150" height="60" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
        <text x="445" y="130" font-size="12" font-weight="bold" fill="#1e40af" text-anchor="middle">4. Server Skeleton</text>
        <text x="445" y="150" font-size="11" fill="#1d4ed8" text-anchor="middle">Deserializes C# object</text>

        <rect x="370" y="20" width="150" height="60" rx="8" fill="#fef2f2" stroke="#ef4444" stroke-width="2"/>
        <text x="445" y="45" font-size="12" font-weight="bold" fill="#991b1b" text-anchor="middle">5. Kitchen Service</text>
        <text x="445" y="65" font-size="11" fill="#b91c1c" text-anchor="middle">Executes HacerPedido()</text>

        <!-- Flow Arrows -->
        <path d="M 95 80 L 95 105" stroke="#10b981" stroke-width="2.5" marker-end="url(#arrow-flow)"/>
        <path d="M 170 135 L 205 135" stroke="#3b82f6" stroke-width="2.5"/>
        <path d="M 335 135 L 370 135" stroke="#8b5cf6" stroke-width="2.5"/>
        <path d="M 445 105 L 445 80" stroke="#3b82f6" stroke-width="2.5" marker-end="url(#arrow-flow)"/>

        <!-- Return path (bottom) -->
        <rect x="180" y="220" width="180" height="35" rx="6" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
        <text x="270" y="242" font-size="11" font-weight="bold" fill="#047857" text-anchor="middle">6. Response travels back in reverse</text>
      </svg>
    </div>

    <div class="callout callout-blue">
      <div class="callout-title">💡 Marshalling vs Unmarshalling</div>
      <div class="callout-body"><strong>Marshalling</strong> packs a C# object into binary bytes for transmission. <strong>Unmarshalling</strong> unpacks binary bytes back into a live C# object.</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Section 4 · Communication Flow</span>
    <span class="footer-right">Page 7</span>
  </div>
</div>

<!-- PAGE 8: THE .PROTO FILE: MESSAGES & FIELD NUMBERS -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Section 5 · The .proto Contract</span>
    <h1 class="page-title">The .proto File: Messages</h1>
    <h2 class="page-subtitle">The agreement that client and server both honor</h2>

    <p>The <code>.proto</code> file uses Protocol Buffers syntax to define all exchanged messages:</p>

    <pre class="code-block"><span class="code-kw">syntax</span> = <span class="code-str">"proto3"</span>;

<span class="code-kw">message</span> <span class="code-fn">PlatoPedido</span> {
  <span class="code-kw">string</span> nombre = <span class="code-num">1</span>;    <span class="code-cm">// Field tag 1</span>
  <span class="code-kw">int32</span> cantidad = <span class="code-num">2</span>;   <span class="code-cm">// Field tag 2</span>
}</pre>

    <p><strong>What do <code>= 1;</code> and <code>= 2;</code> mean?</strong></p>
    <p>These are <strong>binary field tags</strong>, NOT default values or array indexes!</p>
    <p>In the binary packet, gRPC sends the single number <code>1</code> instead of the text <code>"nombre"</code>. This keeps messages tiny.</p>

    <div class="callout callout-red">
      <div class="callout-title">⚠️ Warning: Never renumber fields!</div>
      <div class="callout-body">Never swap tag numbers after releasing code. If tag 1 was a string, renumbering it causes servers to read corrupted data!</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Section 5 · The .proto Contract</span>
    <span class="footer-right">Page 8</span>
  </div>
</div>

<!-- PAGE 9: THE .PROTO FILE: SERVICES & RPCS -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Section 5 · Services & RPCs</span>
    <h1 class="page-title">The .proto File: Services</h1>
    <h2 class="page-subtitle">Declaring the kitchen's public capabilities</h2>

    <p>A <strong>service</strong> is the menu of operations available on the server. Each operation is an <strong>rpc</strong>:</p>

    <pre class="code-block"><span class="code-kw">service</span> <span class="code-fn">RestauranteService</span> {
  <span class="code-cm">// 1. Customer places an order</span>
  <span class="code-kw">rpc</span> <span class="code-fn">HacerPedido</span> (PedidoRequest) <span class="code-kw">returns</span> (PedidoResponse);

  <span class="code-cm">// 2. Customer checks order status</span>
  <span class="code-kw">rpc</span> <span class="code-fn">ConsultarEstadoPedido</span> (ConsultaRequest) <span class="code-kw">returns</span> (EstadoResponse);

  <span class="code-cm">// 3. Courier waits and claims an order</span>
  <span class="code-kw">rpc</span> <span class="code-fn">TomarPedidoParaRepartir</span> (google.protobuf.Empty) <span class="code-kw">returns</span> (PedidoResponse);

  <span class="code-cm">// 4. Customer inspects order dishes</span>
  <span class="code-kw">rpc</span> <span class="code-fn">ConsultarPlatosPedido</span> (ConsultaRequest) <span class="code-kw">returns</span> (PedidoResponse);
}</pre>

    <p>These are <strong>Unary RPCs</strong>: the client sends one request and receives one response.</p>

    <div class="callout callout-amber">
      <div class="callout-title">📝 Notes: Original Lab Dots (...)</div>
      <div class="callout-body">The lab left field types and tags as placeholder dots <code>...</code>. In Step 1.5, we give you the exact, complete types for every field!</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Section 5 · Services & RPCs</span>
    <span class="footer-right">Page 9</span>
  </div>
</div>

<!-- PAGE 10: CODE GENERATION (PROTOC) -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Section 6 · Code Generation</span>
    <h1 class="page-title">Code Generation (protoc)</h1>
    <h2 class="page-subtitle">Why we never write network serialization by hand</h2>

    <p>Writing network sockets and binary encoders manually takes weeks. The <strong>protoc compiler</strong> generates all code automatically:</p>

    <!-- Diagram 3: Code generation -->
    <div style="margin: 6px 0 10px 0; text-align: center;">
      <svg width="490" height="210" viewBox="0 0 540 230">
        <rect x="5" y="5" width="530" height="220" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
        
        <!-- Input file -->
        <rect x="25" y="35" width="130" height="150" rx="8" fill="#fff1f2" stroke="#f43f5e" stroke-width="2"/>
        <text x="90" y="70" font-size="28" text-anchor="middle">📄</text>
        <text x="90" y="100" font-size="13" font-weight="bold" fill="#be123c" text-anchor="middle">restaurante.proto</text>
        <text x="90" y="125" font-size="11" fill="#475569" text-anchor="middle">Your clean contract</text>
        <text x="90" y="145" font-size="10" fill="#64748b" text-anchor="middle">~30 lines of text</text>

        <!-- Arrow & Compiler -->
        <path d="M 160 110 L 210 110" stroke="#f43f5e" stroke-width="2.5"/>
        <rect x="215" y="65" width="110" height="90" rx="8" fill="#0f172a" stroke="#334155" stroke-width="2"/>
        <text x="270" y="102" font-size="22" text-anchor="middle">⚙️</text>
        <text x="270" y="125" font-size="13" font-weight="bold" fill="#38bdf8" text-anchor="middle">protoc</text>
        <text x="270" y="142" font-size="10" fill="#94a3b8" text-anchor="middle">compiler</text>
        <path d="M 330 110 L 375 110" stroke="#38bdf8" stroke-width="2.5"/>

        <!-- Generated C# files -->
        <rect x="380" y="35" width="135" height="150" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="2"/>
        <text x="447" y="65" font-size="22" text-anchor="middle">⚡</text>
        <text x="447" y="90" font-size="12" font-weight="bold" fill="#065f46" text-anchor="middle">Auto-Generated C#</text>
        <text x="447" y="112" font-size="10" fill="#047857" text-anchor="middle">• Client Stub</text>
        <text x="447" y="128" font-size="10" fill="#047857" text-anchor="middle">• Server Base</text>
        <text x="447" y="144" font-size="10" fill="#047857" text-anchor="middle">• Message classes</text>
        <text x="447" y="165" font-size="10" font-weight="bold" fill="#059669" text-anchor="middle">~2,000 lines</text>
      </svg>
    </div>

    <div class="callout callout-green">
      <div class="callout-title">📌 Remember: Never edit generated code!</div>
      <div class="callout-body">Whenever you run <code>dotnet build</code>, <code>Grpc.Tools</code> regenerates these files. Edit <code>restaurante.proto</code> instead!</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Section 6 · Code Generation</span>
    <span class="footer-right">Page 10</span>
  </div>
</div>

<!-- PAGE 11: THE LAB STEP BY STEP - ROADMAP -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Section 7 · The Lab Step by Step</span>
    <h1 class="page-title">Lab Roadmap</h1>
    <h2 class="page-subtitle">Your step-by-step path from zero to complete</h2>

    <p>We will implement the lab across four clear phases:</p>

    <!-- Diagram 4: Lab Workflow from start to finish -->
    <div style="margin: 4px 0 10px 0; text-align: center;">
      <svg width="490" height="220" viewBox="0 0 540 240">
        <rect x="5" y="5" width="530" height="230" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
        
        <!-- Step 1 -->
        <rect x="25" y="25" width="230" height="85" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
        <text x="40" y="52" font-size="13" font-weight="bold" fill="#1e40af">PHASE 1: Restaurante</text>
        <text x="40" y="72" font-size="11" fill="#1d4ed8">• Configure Kestrel HTTP/2</text>
        <text x="40" y="90" font-size="11" fill="#1d4ed8">• restaurante.proto & Service logic</text>

        <!-- Step 2 -->
        <rect x="285" y="25" width="230" height="85" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="2"/>
        <text x="300" y="52" font-size="13" font-weight="bold" fill="#065f46">PHASE 2: Cliente</text>
        <text x="300" y="72" font-size="11" fill="#047857">• ConnectAsync with HTTP/2 switch</text>
        <text x="300" y="90" font-size="11" fill="#047857">• HacerPedido & ConsultarEstado</text>

        <!-- Step 3 -->
        <rect x="25" y="130" width="230" height="85" rx="8" fill="#fffbeb" stroke="#f59e0b" stroke-width="2"/>
        <text x="40" y="157" font-size="13" font-weight="bold" fill="#92400e">PHASE 3: Repartidor</text>
        <text x="40" y="177" font-size="11" fill="#b45309">• Channel & Certificate bypass</text>
        <text x="40" y="195" font-size="11" fill="#b45309">• TomarPedidoParaRepartir loop</text>

        <!-- Step 4 -->
        <rect x="285" y="130" width="230" height="85" rx="8" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="2"/>
        <text x="300" y="157" font-size="13" font-weight="bold" fill="#5b21b6">PHASE 4: Launch & Test</text>
        <text x="300" y="177" font-size="11" fill="#6d28d9">• Start Kitchen in Terminal 1</text>
        <text x="300" y="195" font-size="11" fill="#6d28d9">• Start Courier & Place Orders!</text>
      </svg>
    </div>

    <div class="callout callout-amber">
      <div class="callout-title">📝 Notes: Project Templates</div>
      <div class="callout-body">The lab uses starter folders from Campus Virtual. If building from scratch, run <code>dotnet new console</code> and add the <code>Grpc.AspNetCore</code> NuGet package.</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Section 7 · Lab Roadmap</span>
    <span class="footer-right">Page 11</span>
  </div>
</div>

<!-- PAGE 12: STEP 1.1 & 1.2: KESTREL & ADDGRPC -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Lab Step 1.1 & 1.2 · Server Setup</span>
    <h1 class="page-title">Configuring Kestrel</h1>
    <h2 class="page-subtitle">Enabling HTTP/2 without TLS on port 5000</h2>

    <p><strong>Goal:</strong> Configure Kestrel to listen on HTTP/2 without TLS on port 5000 and enable gRPC support.</p>
    <p><strong>What to do:</strong> In <code>Restaurante/Program.cs</code>, add before <code>builder.Build()</code>:</p>

    <pre class="code-block"><span class="code-cm">// Step 1.1: Listen on port 5000 using HTTP/2 without TLS</span>
builder.WebHost.<span class="code-fn">ConfigureKestrel</span>(options => {
    options.<span class="code-fn">ListenLocalhost</span>(<span class="code-num">5000</span>, o => o.Protocols = HttpProtocols.Http2);
});

<span class="code-cm">// Step 1.2: Register gRPC middleware in ASP.NET Core</span>
builder.Services.<span class="code-fn">AddGrpc</span>();</pre>

    <p><strong>Why we do it:</strong> Standard web traffic uses HTTP/1.1. gRPC requires HTTP/2. This setting enables plain HTTP/2 for local lab development.</p>
    <p><strong>Expected result:</strong> Server configures Kestrel for HTTP/2 on port 5000.</p>

    <div class="callout callout-red">
      <div class="callout-title">⚠️ Warning: Missing Http2 protocol setting</div>
      <div class="callout-body">If you omit <code>o.Protocols = HttpProtocols.Http2</code>, Kestrel uses HTTP/1.1 and all gRPC calls fail with status code 426!</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Step 1.1 & 1.2 · Server Setup</span>
    <span class="footer-right">Page 12</span>
  </div>
</div>

<!-- PAGE 13: STEP 1.3 & 1.4: SINGLETON & MAPPING -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Lab Step 1.3 & 1.4 · Service Registration</span>
    <h1 class="page-title">Singleton & Endpoint Mapping</h1>
    <h2 class="page-subtitle">Sharing one kitchen queue across all incoming requests</h2>

    <p><strong>Goal:</strong> Register <code>RestauranteService</code> as a Singleton and map gRPC routes to it.</p>
    <p><strong>What to do:</strong> In <code>Restaurante/Program.cs</code>:</p>

    <pre class="code-block"><span class="code-cm">// Step 1.3: Register service as Singleton to preserve state</span>
builder.Services.<span class="code-fn">AddSingleton</span>&lt;RestauranteService&gt;();

<span class="code-kw">var</span> app = builder.<span class="code-fn">Build</span>();

<span class="code-cm">// Step 1.4: Map gRPC endpoints and fallback route</span>
app.<span class="code-fn">MapGrpcService</span>&lt;RestauranteService&gt;();
app.<span class="code-fn">MapGet</span>(<span class="code-str">"/"</span>, () => <span class="code-str">"Servidor gRPC del Restaurante ejecutándose..."</span>);</pre>

    <p><strong>Why we do it:</strong> A <strong>Singleton</strong> creates only one service instance. All orders stay in the same memory queue!</p>
    <p><strong>Expected result:</strong> Server maps incoming RPC calls to our singleton service.</p>

    <div class="callout callout-blue">
      <div class="callout-title">💡 Why Singleton instead of Transient?</div>
      <div class="callout-body">If registered as <code>Transient</code>, ASP.NET creates a new service instance for every call, and orders vanish instantly!</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Step 1.3 & 1.4 · Service Registration</span>
    <span class="footer-right">Page 13</span>
  </div>
</div>

<!-- PAGE 14: STEP 1.5 & 1.6: PROTO FILE IMPLEMENTATION -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Lab Step 1.5 & 1.6 · Proto Contract</span>
    <h1 class="page-title">Writing restaurante.proto</h1>
    <h2 class="page-subtitle">Completing the contract with exact types and field tags</h2>

    <p><strong>Goal:</strong> Define all messages and RPC methods in <code>restaurante.proto</code>.</p>
    <p><strong>What to do:</strong> In <code>Restaurante/Protos/restaurante.proto</code>, add:</p>

    <pre class="code-block"><span class="code-kw">syntax</span> = <span class="code-str">"proto3"</span>;
<span class="code-kw">import</span> <span class="code-str">"google/protobuf/empty.proto"</span>;
<span class="code-kw">option</span> csharp_namespace = <span class="code-str">"Restaurante"</span>;

<span class="code-kw">message</span> <span class="code-fn">PlatoPedido</span> { <span class="code-kw">string</span> nombre = <span class="code-num">1</span>; <span class="code-kw">int32</span> cantidad = <span class="code-num">2</span>; }
<span class="code-kw">message</span> <span class="code-fn">PedidoRequest</span> { <span class="code-kw">repeated</span> PlatoPedido platos = <span class="code-num">1</span>; <span class="code-kw">int32</span> distancia = <span class="code-num">2</span>; }
<span class="code-kw">message</span> <span class="code-fn">PedidoResponse</span> { <span class="code-kw">int32</span> id_pedido = <span class="code-num">1</span>; <span class="code-kw">string</span> mensaje = <span class="code-num">2</span>; }
<span class="code-kw">message</span> <span class="code-fn">ConsultaRequest</span> { <span class="code-kw">int32</span> id_pedido = <span class="code-num">1</span>; }
<span class="code-kw">message</span> <span class="code-fn">EstadoResponse</span> { <span class="code-kw">string</span> estado = <span class="code-num">1</span>; <span class="code-kw">string</span> mensaje = <span class="code-num">2</span>; <span class="code-kw">int32</span> tiempo_estimado = <span class="code-num">3</span>; }</pre>

    <p><strong>Why we do it:</strong> Gives <code>protoc</code> the blueprint to generate type-safe C# classes.</p>
    <p><strong>Expected result:</strong> <code>dotnet build</code> compiles without errors.</p>

    <div class="callout callout-amber">
      <div class="callout-title">📝 Notes: Missing Import in Lab</div>
      <div class="callout-body">The lab uses <code>google.protobuf.Empty</code> for couriers, but omits <code>import "google/protobuf/empty.proto";</code>. Always include this import at the top!</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Step 1.5 & 1.6 · Proto Contract</span>
    <span class="footer-right">Page 14</span>
  </div>
</div>

<!-- PAGE 15: STEP 1.7: STATE & CONCURRENCY VARIABLES -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Lab Step 1.7 · State & Synchronization</span>
    <h1 class="page-title">Concurrency & Shared State</h1>
    <h2 class="page-subtitle">Protecting the order queue from race conditions</h2>

    <p><strong>Goal:</strong> Declare and initialize the shared queue, lock object, and semaphore.</p>
    <p><strong>What to do:</strong> In <code>Restaurante/Services/RestauranteService.cs</code>:</p>

    <pre class="code-block"><span class="code-kw">private readonly</span> ConcurrentQueue&lt;Pedido&gt; _ordersQueue = <span class="code-kw">new</span>();
<span class="code-kw">private const int</span> MaxQueueCapacity = <span class="code-num">10</span>;
<span class="code-kw">private readonly</span> SemaphoreSlim _readyOrdersSemaphore = <span class="code-kw">new</span>(<span class="code-num">0</span>);
<span class="code-kw">private readonly</span> <span class="code-kw">object</span> _takeLock = <span class="code-kw">new</span>();
<span class="code-kw">private int</span> _orderID = <span class="code-num">1</span>;</pre>

    <p><strong>Why we do it:</strong> Customers and couriers call the kitchen simultaneously. <code>SemaphoreSlim</code> signals sleeping couriers when food is ready. <code>_takeLock</code> prevents race conditions.</p>
    <p><strong>Expected result:</strong> Thread-safe variables ready in the kitchen.</p>

    <div class="callout callout-amber">
      <div class="callout-title">📝 Notes: Semaphore Initial Count = 0</div>
      <div class="callout-body">Always initialize <code>_readyOrdersSemaphore</code> to <code>0</code>! Couriers must sleep until the first order is placed.</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Step 1.7 · State & Synchronization</span>
    <span class="footer-right">Page 15</span>
  </div>
</div>

<!-- PAGE 16: STEP 1.8: IMPLEMENTING HACERPEDIDO -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Lab Step 1.8 · Kitchen Logic</span>
    <h1 class="page-title">Implementing HacerPedido</h1>
    <h2 class="page-subtitle">Safely storing orders and ringing the courier bell</h2>

    <p><strong>Goal:</strong> Accept customer orders safely and wake up waiting couriers.</p>
    <p><strong>What to do:</strong> In <code>RestauranteService.cs</code>:</p>

    <pre class="code-block"><span class="code-kw">public override</span> Task&lt;PedidoResponse&gt; <span class="code-fn">HacerPedido</span>(PedidoRequest req, ServerCallContext ctx) {
  <span class="code-kw">lock</span> (_takeLock) {
    <span class="code-kw">if</span> (_ordersQueue.Count &lt; MaxQueueCapacity) {
      <span class="code-kw">var</span> p = <span class="code-kw">new</span> Pedido(_orderID, req.Platos.ToList(), req.Distancia);
      _ordersQueue.<span class="code-fn">Enqueue</span>(p);
      _orderID++;
      _readyOrdersSemaphore.<span class="code-fn">Release</span>(); <span class="code-cm">// Ring bell: wake 1 courier!</span>
      <span class="code-kw">return</span> Task.<span class="code-fn">FromResult</span>(<span class="code-kw">new</span> PedidoResponse {
        IdPedido = p.Id, Mensaje = <span class="code-str">"Pedido en preparación"</span>
      });
    }
  }
  <span class="code-kw">throw new</span> RpcException(<span class="code-kw">new</span> Status(StatusCode.ResourceExhausted, <span class="code-str">"Cola llena"</span>));
}</pre>

    <p><strong>Why we do it:</strong> <code>lock</code> prevents ID conflicts. <code>Release()</code> increments the semaphore to awaken one waiting delivery driver.</p>
    <p><strong>Expected result:</strong> Returns new Order ID and wakes a driver.</p>

    <div class="callout callout-green">
      <div class="callout-title">📌 Remember: The Semaphore Bell</div>
      <div class="callout-body"><code>_readyOrdersSemaphore.Release()</code> is the chef ringing the counter bell. One waiting courier wakes up instantly!</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Step 1.8 · Kitchen Logic</span>
    <span class="footer-right">Page 16</span>
  </div>
</div>

<!-- PAGE 17: STEP 1.9 & 1.10: CONSULTARESTADO & TOMARPEDIDO -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Lab Step 1.9 & 1.10 · Status & Delivery</span>
    <h1 class="page-title">Status Check & Pickup</h1>
    <h2 class="page-subtitle">Tracking food and dispatching couriers</h2>

    <p><strong>Goal:</strong> Allow customers to track orders and couriers to claim ready food.</p>
    <p><strong>What to do:</strong> In <code>RestauranteService.cs</code>:</p>

    <pre class="code-block"><span class="code-kw">public override</span> Task&lt;EstadoResponse&gt; <span class="code-fn">ConsultarEstadoPedido</span>(ConsultaRequest req, ServerCallContext ctx) {
  <span class="code-kw">var</span> p = _ordersQueue.<span class="code-fn">FirstOrDefault</span>(o => o.Id == req.IdPedido);
  <span class="code-kw">if</span> (p == <span class="code-kw">null</span>) <span class="code-kw">throw new</span> RpcException(<span class="code-kw">new</span> Status(StatusCode.NotFound, <span class="code-str">"Pedido no existe"</span>));
  <span class="code-kw">return</span> Task.<span class="code-fn">FromResult</span>(<span class="code-kw">new</span> EstadoResponse { Estado = p.Estado, TiempoEstimado = p.TiempoEstimado });
}

<span class="code-kw">public override async</span> Task&lt;PedidoResponse&gt; <span class="code-fn">TomarPedidoParaRepartir</span>(Empty req, ServerCallContext ctx) {
  <span class="code-kw">await</span> _readyOrdersSemaphore.<span class="code-fn">WaitAsync</span>(); <span class="code-cm">// Sleep until food is ready!</span>
  <span class="code-kw">lock</span> (_takeLock) {
    <span class="code-kw">if</span> (_ordersQueue.<span class="code-fn">TryDequeue</span>(<span class="code-kw">out var</span> p)) {
      p.Estado = <span class="code-str">"En reparto"</span>;
      <span class="code-kw">return new</span> PedidoResponse { IdPedido = p.Id, Mensaje = <span class="code-str">"Pedido tomado"</span> };
    }
  }
  <span class="code-kw">throw new</span> RpcException(<span class="code-kw">new</span> Status(StatusCode.NotFound, <span class="code-str">"Sin pedidos disponibles"</span>));
}</pre>

    <p><strong>Why we do it:</strong> <code>WaitAsync()</code> suspends the courier call asynchronously with zero CPU waste until an order is ready.</p>
    <p><strong>Expected result:</strong> Couriers take orders in strict FIFO order.</p>

    <div class="callout callout-blue">
      <div class="callout-title">💡 Why WaitAsync() instead of a while loop?</div>
      <div class="callout-body">A <code>while(true)</code> loop burns 100% CPU polling. <code>WaitAsync()</code> pauses the thread at zero cost!</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Step 1.9 & 1.10 · Status & Delivery</span>
    <span class="footer-right">Page 17</span>
  </div>
</div>

<!-- PAGE 18: STEP 2.1 - 2.3: CLIENTE CONNECTION -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Lab Step 2.1 – 2.3 · Cliente Project</span>
    <h1 class="page-title">Connecting the Customer</h1>
    <h2 class="page-subtitle">Creating the channel and client stub</h2>

    <p><strong>Goal:</strong> Initialize the gRPC channel and create the client stub.</p>
    <p><strong>What to do:</strong> In <code>Cliente/Services/RestauranteClientService.cs</code>:</p>

    <pre class="code-block"><span class="code-kw">public async</span> Task <span class="code-fn">ConnectAsync</span>() {
  <span class="code-kw">if</span> (_serverAddress.<span class="code-fn">StartsWith</span>(<span class="code-str">"http://"</span>, StringComparison.OrdinalIgnoreCase)) {
    AppContext.<span class="code-fn">SetSwitch</span>(<span class="code-str">"System.Net.Http.SocketsHttpHandler.Http2UnencryptedSupport"</span>, <span class="code-kw">true</span>);
  }
  _channel = GrpcChannel.<span class="code-fn">ForAddress</span>(_serverAddress, <span class="code-kw">new</span> GrpcChannelOptions());
  _client = <span class="code-kw">new</span> RestauranteService.RestauranteServiceClient(_channel);
  Console.<span class="code-fn">WriteLine</span>($<span class="code-str">"Conectado al servidor en {_serverAddress}"</span>);
}

<span class="code-kw">public async</span> Task <span class="code-fn">DisconnectAsync</span>() {
  <span class="code-kw">if</span> (_channel != <span class="code-kw">null</span>) { <span class="code-kw">await</span> _channel.<span class="code-fn">ShutdownAsync</span>(); }
}</pre>

    <p><strong>Why we do it:</strong> .NET blocks unencrypted HTTP/2 for security. <code>SetSwitch</code> unlocks it for local labs.</p>
    <p><strong>Expected result:</strong> Prints <code>"Conectado al servidor en http://localhost:5000"</code>.</p>

    <div class="callout callout-blue">
      <div class="callout-title">💡 What is RestauranteServiceClient?</div>
      <div class="callout-body">It is the auto-generated <strong>Client Stub</strong> (the waiter). It exposes C# methods that package requests and transmit them over HTTP/2.</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Step 2.1 – 2.3 · Cliente Project</span>
    <span class="footer-right">Page 18</span>
  </div>
</div>

<!-- PAGE 19: STEP 2.4 & 2.5: CLIENTE OPERATIONS -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Lab Step 2.4 & 2.5 · Cliente Operations</span>
    <h1 class="page-title">Placing & Tracking Orders</h1>
    <h2 class="page-subtitle">Invoking remote methods and handling errors</h2>

    <p><strong>Goal:</strong> Implement <code>HacerPedidoAsync</code> and <code>ConsultarEstadoPedidoAsync</code> in the client.</p>
    <p><strong>What to do:</strong> In <code>RestauranteClientService.cs</code>:</p>

    <pre class="code-block"><span class="code-kw">public async</span> Task&lt;PedidoResponse&gt; <span class="code-fn">HacerPedidoAsync</span>(List&lt;PlatoPedido&gt; platos, <span class="code-kw">int</span> dist) {
  <span class="code-kw">var</span> req = <span class="code-kw">new</span> PedidoRequest { Distancia = dist };
  req.Platos.<span class="code-fn">AddRange</span>(platos);
  <span class="code-kw">try</span> {
    <span class="code-kw">var</span> res = <span class="code-kw">await</span> _client.<span class="code-fn">HacerPedidoAsync</span>(req);
    Console.<span class="code-fn">WriteLine</span>($<span class="code-str">"Pedido #{res.IdPedido}: {res.Mensaje}"</span>);
    <span class="code-kw">return</span> res;
  } <span class="code-kw">catch</span> (RpcException ex) { Console.<span class="code-fn">WriteLine</span>($<span class="code-str">"Error: {ex.Status.Detail}"</span>); <span class="code-kw">throw</span>; }
}

<span class="code-kw">public async</span> Task&lt;EstadoResponse&gt; <span class="code-fn">ConsultarEstadoPedidoAsync</span>(<span class="code-kw">int</span> id) {
  <span class="code-kw">try</span> {
    <span class="code-kw">var</span> res = <span class="code-kw">await</span> _client.<span class="code-fn">ConsultarEstadoPedidoAsync</span>(<span class="code-kw">new</span> ConsultaRequest { IdPedido = id });
    Console.<span class="code-fn">WriteLine</span>($<span class="code-str">"Estado: {res.Estado}, Tiempo: {res.TiempoEstimado} min"</span>);
    <span class="code-kw">return</span> res;
  } <span class="code-kw">catch</span> (RpcException ex) { Console.<span class="code-fn">WriteLine</span>($<span class="code-str">"Error: {ex.Status.Detail}"</span>); <span class="code-kw">throw</span>; }
}</pre>

    <p><strong>Why we do it:</strong> Sends typed requests over the network and catches remote exceptions.</p>
    <p><strong>Expected result:</strong> Customer can place orders and query cooking time.</p>

    <div class="callout callout-green">
      <div class="callout-title">📌 Remember: Repeated Protobuf Fields</div>
      <div class="callout-body">Protobuf <code>repeated</code> lists are read-only collections in C#. Populate them using <code>.AddRange()</code> instead of direct assignment!</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Step 2.4 & 2.5 · Cliente Operations</span>
    <span class="footer-right">Page 19</span>
  </div>
</div>

<!-- PAGE 20: STEP 3.1 & 3.2: REPARTIDOR (COURIER) -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Lab Step 3.1 & 3.2 · Repartidor Project</span>
    <h1 class="page-title">The Courier Worker</h1>
    <h2 class="page-subtitle">Waiting patiently for orders to deliver</h2>

    <p><strong>Goal:</strong> Connect the courier app and wait for available orders.</p>
    <p><strong>What to do:</strong> In <code>Repartidor/Program.cs</code>:</p>

    <pre class="code-block"><span class="code-kw">var</span> httpHandler = <span class="code-kw">new</span> HttpClientHandler();
httpHandler.ServerCertificateCustomValidationCallback = 
    HttpClientHandler.DangerousAcceptAnyServerCertificateValidator;

<span class="code-kw">var</span> channel = GrpcChannel.<span class="code-fn">ForAddress</span>(<span class="code-str">"http://localhost:5000"</span>,
    <span class="code-kw">new</span> GrpcChannelOptions { HttpHandler = httpHandler });
<span class="code-kw">var</span> client = <span class="code-kw">new</span> RestauranteService.RestauranteServiceClient(channel);

<span class="code-cm">// Claim an order</span>
<span class="code-kw">try</span> {
  Console.<span class="code-fn">WriteLine</span>(<span class="code-str">"Esperando pedidos disponibles..."</span>);
  <span class="code-kw">var</span> res = <span class="code-kw">await</span> client.<span class="code-fn">TomarPedidoParaRepartirAsync</span>(<span class="code-kw">new</span> Empty());
  Console.<span class="code-fn">WriteLine</span>($<span class="code-str">"¡Pedido #{res.IdPedido} asignado para entrega!"</span>);
} <span class="code-kw">catch</span> (RpcException ex) { Console.<span class="code-fn">WriteLine</span>($<span class="code-str">"Error: {ex.Status.Detail}"</span>); }</pre>

    <p><strong>Why we do it:</strong> Courier calls the server and sleeps until the kitchen rings the bell.</p>
    <p><strong>Expected result:</strong> When a customer orders, the courier instantly receives it.</p>

    <div class="callout callout-green">
      <div class="callout-title">📌 Remember: Multiple Couriers Scale Safely</div>
      <div class="callout-body">If multiple couriers run simultaneously, each order is claimed by exactly one courier thanks to <code>SemaphoreSlim</code> and <code>lock</code>!</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Step 3.1 & 3.2 · Repartidor Project</span>
    <span class="footer-right">Page 20</span>
  </div>
</div>

<!-- PAGE 21: STEP 4: RUNNING THE DISTRIBUTED SYSTEM -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Lab Step 4 · System Launch</span>
    <h1 class="page-title">Launching the System</h1>
    <h2 class="page-subtitle">Watching all three distributed programs collaborate</h2>

    <p><strong>Goal:</strong> Run all three applications across separate terminals and watch them interact.</p>
    <p><strong>What to do:</strong> Open three terminal tabs in VS Code or PowerShell:</p>

    <pre class="code-block"><span class="code-cm"># Terminal 1: Start the Kitchen Server first</span>
dotnet run --project Restaurante

<span class="code-cm"># Terminal 2: Start the Delivery Courier (waits patiently)</span>
dotnet run --project Repartidor

<span class="code-cm"># Terminal 3: Start the Customer and place an order!</span>
dotnet run --project Cliente</pre>

    <p><strong>Why we do it:</strong> Verifies real end-to-end communication across 3 distinct processes over HTTP/2.</p>
    <p><strong>Expected result:</strong> Placing an order in Terminal 3 immediately wakes up Terminal 2 to deliver it!</p>

    <div class="callout callout-green">
      <div class="callout-title">📌 Remember: Launch Order Matters!</div>
      <div class="callout-body">Always start the <strong>Restaurante server first</strong> so that clients and couriers have an active server to connect to.</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Step 4 · System Launch</span>
    <span class="footer-right">Page 21</span>
  </div>
</div>

<!-- PAGE 22: COMMON MISTAKES & FIXES -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Section 8 · Troubleshooting</span>
    <h1 class="page-title">Common Mistakes & Fixes</h1>
    <h2 class="page-subtitle">How to diagnose and solve the top four beginner traps</h2>

    <p>If something does not work as expected, check these four common pitfalls:</p>

    <div class="callout callout-red">
      <div class="callout-title">Trap 1: Orders disappear immediately</div>
      <div class="callout-body"><strong>Cause:</strong> Registered service as <code>AddScoped</code> or <code>AddTransient</code>.<br><strong>Fix:</strong> Use <code>builder.Services.AddSingleton&lt;RestauranteService&gt;()</code>.</div>
    </div>

    <div class="callout callout-red">
      <div class="callout-title">Trap 2: HTTP 426 or "Bad HTTP/1.1 Request"</div>
      <div class="callout-body"><strong>Cause:</strong> Kestrel defaulted to HTTP/1.1 without TLS.<br><strong>Fix:</strong> Set <code>o.Protocols = HttpProtocols.Http2</code> and set <code>Http2UnencryptedSupport</code> switch to <code>true</code>.</div>
    </div>

    <div class="callout callout-red">
      <div class="callout-title">Trap 3: Courier claims empty order right away</div>
      <div class="callout-body"><strong>Cause:</strong> <code>SemaphoreSlim</code> was initialized with count 1 instead of 0.<br><strong>Fix:</strong> Initialize with <code>new SemaphoreSlim(0)</code> so couriers sleep until food is ready.</div>
    </div>

    <div class="callout callout-red">
      <div class="callout-title">Trap 4: protoc fails with "Empty is not defined"</div>
      <div class="callout-body"><strong>Cause:</strong> Missing protobuf standard import.<br><strong>Fix:</strong> Add <code>import "google/protobuf/empty.proto";</code> at top of <code>restaurante.proto</code>.</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Section 8 · Troubleshooting</span>
    <span class="footer-right">Page 22</span>
  </div>
</div>

<!-- PAGE 23: ONE-PAGE CHEAT SHEET -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Section 9 · Quick Reference</span>
    <h1 class="page-title">1-Page Cheat Sheet</h1>
    <h2 class="page-subtitle">The entire gRPC distributed lab at a single glance</h2>

    <table class="simple-table">
      <tr><th>gRPC Concept</th><th>Restaurant Analogy</th><th>What it does in C#</th></tr>
      <tr><td><strong>Client</strong></td><td>Hungry Customer</td><td>Console app calling <code>_client.HacerPedidoAsync()</code></td></tr>
      <tr><td><strong>Server</strong></td><td>The Kitchen</td><td>ASP.NET Core host listening on port 5000</td></tr>
      <tr><td><strong>.proto file</strong></td><td>The Menu Contract</td><td>Interface definition used by <code>protoc</code></td></tr>
      <tr><td><strong>Client Stub</strong></td><td>The Waiter</td><td>Auto-generated class serializing calls into bytes</td></tr>
      <tr><td><strong>HTTP/2</strong></td><td>Order Tube</td><td>High-speed binary transport with multiplexing</td></tr>
    </table>

    <table class="simple-table" style="margin-top: 10px;">
      <tr><th>Tool / Method</th><th>Purpose & Golden Rule</th></tr>
      <tr><td><code>AddSingleton</code></td><td>Keeps one shared queue instance in server memory.</td></tr>
      <tr><td><code>lock (_takeLock)</code></td><td>Ensures exclusive access to check capacity and increment IDs.</td></tr>
      <tr><td><code>SemaphoreSlim(0)</code></td><td>Couriers sleep with <code>WaitAsync()</code> until kitchen calls <code>Release()</code>.</td></tr>
      <tr><td><code>ConcurrentQueue&lt;T&gt;</code></td><td>Thread-safe FIFO queue for incoming customer orders.</td></tr>
    </table>

    <div class="callout callout-green">
      <div class="callout-title">📌 Golden Rule</div>
      <div class="callout-body">Never edit generated code by hand. Modify <code>restaurante.proto</code> and let <code>dotnet build</code> do the generation!</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Section 9 · Cheat Sheet</span>
    <span class="footer-right">Page 23</span>
  </div>
</div>

<!-- PAGE 24: QUIZ QUESTIONS & ANSWERS -->
<div class="page">
  <div class="page-content">
    <span class="header-tag">Section 9 · Knowledge Check</span>
    <h1 class="page-title">5 Quiz Questions</h1>
    <h2 class="page-subtitle">Test and prove your understanding of gRPC</h2>

    <div style="font-size: 13.5pt; line-height: 1.35; margin-bottom: 6px;">
      <p style="margin-bottom: 4px;"><strong>Q1: What do numbers like <code>= 1;</code> in a .proto file represent?</strong><br>
      <span style="color: #047857;"><strong>Ans:</strong> Unique binary field tags on the wire, not default values!</span></p>

      <p style="margin-bottom: 4px;"><strong>Q2: Why must <code>RestauranteService</code> be a Singleton?</strong><br>
      <span style="color: #047857;"><strong>Ans:</strong> So all clients and couriers share the same order queue in memory.</span></p>

      <p style="margin-bottom: 4px;"><strong>Q3: Why use <code>SemaphoreSlim</code> instead of a while loop?</strong><br>
      <span style="color: #047857;"><strong>Ans:</strong> A while loop burns 100% CPU. <code>WaitAsync()</code> sleeps with 0% CPU.</span></p>

      <p style="margin-bottom: 4px;"><strong>Q4: What is the Client Stub's main job?</strong><br>
      <span style="color: #047857;"><strong>Ans:</strong> It serializes objects into binary and hides network complexity.</span></p>

      <p style="margin-bottom: 4px;"><strong>Q5: How does gRPC differ from REST/JSON?</strong><br>
      <span style="color: #047857;"><strong>Ans:</strong> gRPC uses compact binary Protobuf over HTTP/2 instead of text JSON.</span></p>
    </div>

    <div class="callout callout-green" style="text-align: center; margin-top: 6px;">
      <div class="callout-title" style="justify-content: center; font-size: 15pt;">🎉 Congratulations!</div>
      <div class="callout-body" style="font-size: 14pt;">You have mastered distributed systems with gRPC!</div>
    </div>
  </div>
  <div class="page-footer">
    <span class="footer-left">Section 9 · Quiz & Wrap-up</span>
    <span class="footer-right">Page 24</span>
  </div>
</div>

</body>
</html>
"""

# Write HTML file
workspace_dir = r"c:\Users\ssola\systemas distribuidos practice 3"
html_path = os.path.join(workspace_dir, "gRPC_Beginner_Guide.html")
pdf_path = os.path.join(workspace_dir, "gRPC_Beginner_Guide.pdf")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML written to {html_path} ({len(html_content)} bytes)")

# Compile to PDF using Chrome Headless
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
temp_user_dir = os.path.join(os.environ.get("TEMP", r"C:\Windows\Temp"), "chrome-pdf-grpc-guide")

cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    f"--user-data-dir={temp_user_dir}",
    html_path
]

print("Compiling PDF with headless Chrome...")
res = subprocess.run(cmd, capture_output=True, text=True)
print("Exit code:", res.returncode)

if os.path.exists(pdf_path):
    size = os.path.getsize(pdf_path)
    print(f"SUCCESS: PDF generated at {pdf_path} ({size} bytes)")
    reader = pypdf.PdfReader(pdf_path)
    print(f"Total PDF pages: {len(reader.pages)}")
else:
    print("ERROR: PDF was not created!")
