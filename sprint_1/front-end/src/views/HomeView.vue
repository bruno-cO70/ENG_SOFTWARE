<script setup lang="ts">
// sem lógica extra — página estática/marketing
</script>

<template>
  <div class="home">

    <!-- HERO -->
    <section class="hero">
      <div class="hero-bg-glow" />
      <div class="hero-content">
        <p class="eyebrow">Gestão para salões</p>
        <h1>
          Gerencie seu salão<br>
          <span class="highlight">sem complicação</span>
        </h1>
        <p class="lead">Agendamentos, clientes e notificações em um só lugar.</p>

        <div class="hero-actions">
          <router-link to="/cadastro" class="btn primary">Começar agora</router-link>
          <router-link to="/sobre" class="btn ghost">Saiba mais →</router-link>
        </div>
      </div>
    </section>

    <!-- FEATURES -->
    <section class="features">
      <p class="section-label">O que oferecemos</p>
      <h2>Um sistema completo</h2>

      <div class="feature-grid">
        <div class="feature-card">
          <div class="feature-icon">📅</div>
          <h3>Agenda Inteligente</h3>
          <p>Organize horários automaticamente, sem conflitos e sem esforço.</p>
        </div>

        <div class="feature-card featured">
          <div class="feature-icon">📊</div>
          <h3>Gestão Total</h3>
          <p>Controle seu negócio em tempo real com dados claros e precisos.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">🔔</div>
          <h3>Notificações</h3>
          <p>Clientes nunca mais esquecem os agendamentos.</p>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta-section">
      <div class="cta-box">
        <h2>Comece a transformar<br>seu salão hoje</h2>
        <router-link to="/cadastro" class="btn primary large">Criar conta grátis</router-link>
      </div>
    </section>

  </div>
</template>

<style scoped>
.home {
  overflow: hidden;
}

/* ── HERO ── */
.hero {
  position: relative;
  min-height: 92vh;
  display: flex;
  align-items: center;
  padding: 0 80px;
}

.hero-bg-glow {
  position: absolute;
  top: -100px;
  left: 50%;
  transform: translateX(-50%);
  width: 700px;
  height: 700px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(212,175,55,0.08) 0%, transparent 70%);
  pointer-events: none;
}

.hero-content {
  max-width: 640px;
  position: relative;
  z-index: 1;
}

.eyebrow {
  font-size: 11px;
  letter-spacing: 5px;
  text-transform: uppercase;
  color: #d4af37;
  margin-bottom: 20px;
}

h1 {
  font-size: clamp(40px, 6vw, 72px);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -2px;
  margin-bottom: 24px;
}

.highlight {
  background: linear-gradient(135deg, #d4af37, #f1c40f);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.lead {
  font-size: 18px;
  color: #888;
  margin-bottom: 40px;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

/* ── BUTTONS ── */
.btn {
  display: inline-block;
  padding: 14px 32px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.25s;
  letter-spacing: 0.3px;
}

.btn.primary {
  background: linear-gradient(135deg, #d4af37, #f1c40f);
  color: #000;
}

.btn.primary:hover {
  transform: scale(1.04);
  box-shadow: 0 0 28px rgba(212,175,55,0.5);
}

.btn.ghost {
  color: #aaa;
  border: 1px solid rgba(255,255,255,0.12);
}

.btn.ghost:hover {
  border-color: rgba(212,175,55,0.4);
  color: #f1c40f;
}

.btn.large {
  padding: 18px 48px;
  font-size: 17px;
}

/* ── FEATURES ── */
.features {
  padding: 120px 80px;
  text-align: center;
}

.section-label {
  font-size: 11px;
  letter-spacing: 5px;
  text-transform: uppercase;
  color: #d4af37;
  margin-bottom: 12px;
}

.features h2 {
  font-size: 40px;
  font-weight: 700;
  letter-spacing: -1px;
  margin-bottom: 60px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  max-width: 900px;
  margin: 0 auto;
}

.feature-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 20px;
  padding: 36px 28px;
  text-align: left;
  transition: 0.3s;
}

.feature-card:hover {
  border-color: rgba(212,175,55,0.2);
  transform: translateY(-4px);
}

.feature-card.featured {
  border-color: rgba(212,175,55,0.25);
  background: rgba(212,175,55,0.05);
}

.feature-icon {
  font-size: 32px;
  margin-bottom: 18px;
}

.feature-card h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 10px;
}

.feature-card p {
  color: #777;
  font-size: 14px;
  line-height: 1.6;
}

/* ── CTA ── */
.cta-section {
  padding: 100px 80px;
  display: flex;
  justify-content: center;
}

.cta-box {
  background: rgba(212,175,55,0.05);
  border: 1px solid rgba(212,175,55,0.2);
  border-radius: 28px;
  padding: 72px 80px;
  text-align: center;
  max-width: 680px;
  width: 100%;
}

.cta-box h2 {
  font-size: 36px;
  font-weight: 700;
  letter-spacing: -1px;
  margin-bottom: 36px;
  line-height: 1.25;
}
</style>