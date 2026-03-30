<template>
  <div class="page-container">
    <p class="eyebrow">Vantagens</p>
    <h1>Por que escolher o <span class="highlight">HairTime</span>?</h1>
    <ul class="benefits-list">
      <li><strong>✅ Agendamento 24h:</strong> Seus clientes marcam sozinhos.</li>
      <li><strong>✅ Redução de faltas:</strong> Lembretes automáticos.</li>
      <li><strong>✅ Organização total:</strong> Saiba exatamente quanto vai faturar no dia.</li>
    </ul>
  </div>
</template>

<style scoped>
.page-container {
  padding: 120px 80px;
  text-align: center;
  min-height: 80vh;
  max-width: 800px;
  margin: 0 auto;
}
.eyebrow {
  font-size: 12px;
  letter-spacing: 4px;
  text-transform: uppercase;
  color: #d4af37;
  margin-bottom: 16px;
}
h1 {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 40px;
}
.highlight {
  background: linear-gradient(135deg, #d4af37, #f1c40f);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.benefits-list {
  list-style: none;
  padding: 0;
  text-align: left;
  display: inline-block;
}
.benefits-list li {
  font-size: 18px;
  color: #aaa;
  margin-bottom: 16px;
  background: rgba(255, 255, 255, 0.05);
  padding: 16px 24px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.benefits-list strong {
  color: #f1c40f;
}
</style>