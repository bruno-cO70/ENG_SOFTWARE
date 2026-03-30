<template>
  <div class="page-container">
    <p class="eyebrow">Nossa História</p>
    <h1>Sobre o <span class="highlight">HairTime</span></h1>
    <p class="lead">
      Nascemos para simplificar a vida de barbeiros, cabeleireiros e clientes. 
      Chega de agendas de papel bagunçadas e esquecimentos!
    </p>
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
  color: #aaa;
  line-height: 1.6;
}
</style>