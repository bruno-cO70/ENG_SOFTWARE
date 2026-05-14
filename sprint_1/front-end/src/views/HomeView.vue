<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

/* ==========================================
 * HEURÍSTICA 1: Visibilidade do status do sistema
 * ========================================== */
const scrollProgress = ref(0)

const updateScroll = () => {
  const winScroll = document.body.scrollTop || document.documentElement.scrollTop
  const height = document.documentElement.scrollHeight - document.documentElement.clientHeight
  scrollProgress.value = (winScroll / height) * 100
}

onMounted(() => window.addEventListener('scroll', updateScroll))
onUnmounted(() => window.removeEventListener('scroll', updateScroll))

/* ==========================================
 * HEURÍSTICA 8: Estética e design minimalista (Acordeões)
 * ========================================== */
const faqItems = ref([
  { question: "Como funciona o agendamento online?", answer: "Você escolhe o profissional, o serviço e o horário desejado em poucos cliques.", isOpen: false },
  { question: "Posso remarcar meu horário?", answer: "Sim! Pelo seu painel você pode remarcar com até 2h de antecedência.", isOpen: false },
  { question: "Quais marcas de produtos vocês utilizam?", answer: "Trabalhamos apenas com linhas premium reconhecidas internacionalmente.", isOpen: false }
])

function toggleFaq(index: number) {
  /* HEURÍSTICA 3: Controle e liberdade do usuário */
  faqItems.value[index].isOpen = !faqItems.value[index].isOpen
}

/* ==========================================
 * HEURÍSTICA 5 & 9: Prevenção e correção de erros
 * ========================================== */
const leadEmail = ref('')
const isSubmitting = ref(false)
const submitSuccess = ref(false)
const touched = ref(false)

const isEmailValid = computed(() => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return regex.test(leadEmail.value)
})

const emailErrorMsg = computed(() => {
  if (!touched.value || leadEmail.value === '') return ''
  if (!isEmailValid.value) return 'Por favor, insira um e-mail válido.'
  return ''
})

async function handleLeadSubmit() {
  if (!isEmailValid.value) return
  isSubmitting.value = true // HEURÍSTICA 1: Feedback visual de carregamento
  setTimeout(() => {
    isSubmitting.value = false
    submitSuccess.value = true
    leadEmail.value = ''
  }, 1500)
}
</script>

<template>
  <div class="landing-page">
    <div class="scroll-progress-bar" :style="{ height: scrollProgress + '%' }" aria-hidden="true"></div>

    <header class="sticky-nav">
      <div class="nav-content">
        <div class="logo">Hair<span class="gold-text">Time.</span></div>
        <nav class="nav-links">
          <a href="#sobre">Sobre Nós</a>
          <a href="#servicos">Serviços</a>
          <a href="#faq">FAQ</a>
        </nav>
        <router-link to="/agendar" class="btn primary-gold" aria-label="Agendar horário">Agendar</router-link>
      </div>
    </header>

    <main class="content-wrapper">

      <section class="hero-section">
        <div class="glass-card dual-card">
          <div class="dual-content">
            <span class="eyebrow">HairTime Salon</span>
            <h1 class="serif-title">Transforme-se<br>no nosso <span class="gold-text">salão</span></h1>
            <p>Cabelo, penteados, manicure e pedicure. A melhor experiência em beleza com gestão inteligente.</p>
            
            <div class="hero-actions">
              <a href="#servicos" class="btn outline-gold large">Conheça nossos serviços</a>
            </div>
          </div>
          <div class="dual-image image-placeholder-1">
            <span class="image-label"></span>
          </div>
        </div>
      </section>

      <section id="sobre" class="about-section">
        <div class="glass-card dual-card flipped">
          <div class="dual-image image-placeholder-2">
            <span class="image-label"></span>
          </div>
          <div class="dual-content">
            <span class="eyebrow">Sobre nós</span>
            <h2 class="serif-title">Paixão pela <span class="gold-text">beleza</span></h2>
            <p>Nascemos do desejo de fazer a diferença na vida das pessoas, entregando não apenas estética, mas autoestima e bem-estar em um ambiente acolhedor e luxuoso.</p>
            <router-link to="/sobre" class="btn outline-gold">Saiba mais</router-link>
          </div>
        </div>
      </section>

      <section id="servicos" class="services-section">
        <div class="section-header center">
          <span class="eyebrow">Serviços</span>
          <h2 class="serif-title">O que oferecemos</h2>
        </div>

        <div class="features-grid">
          <div class="glass-card service-card">
            <div class="card-img placeholder-corte"></div>
            <h3 class="serif-title small">Corte de cabelo</h3>
            <p>Realce sua beleza e autoconfiança com cortes personalizados e alinhados às tendências.</p>
            <router-link to="/servicos" class="btn ghost-gold">Ver detalhes</router-link>
          </div>

          <div class="glass-card service-card featured">
            <div class="card-img placeholder-cor"></div>
            <h3 class="serif-title small">Coloração Premium</h3>
            <p>Eleve sua autoconfiança através de cores deslumbrantes com produtos importados.</p>
            <router-link to="/servicos" class="btn ghost-gold">Ver detalhes</router-link>
          </div>

          <div class="glass-card service-card">
            <div class="card-img placeholder-unhas"></div>
            <h3 class="serif-title small">Manicure e Pedicure</h3>
            <p>Oferecemos o melhor tratamento para a saúde e estética das suas mãos e pés.</p>
            <router-link to="/servicos" class="btn ghost-gold">Ver detalhes</router-link>
          </div>
        </div>
      </section>

      <section id="faq" class="faq-section">
        <div class="glass-card faq-container">
          <h2 class="serif-title">Dúvidas Frequentes</h2>
          <div class="faq-list">
            <div 
              v-for="(item, index) in faqItems" 
              :key="index" 
              class="faq-item"
              :class="{ open: item.isOpen }"
            >
              <button class="faq-question" @click="toggleFaq(index)" :aria-expanded="item.isOpen">
                <span class="serif-title small">{{ item.question }}</span>
                <span class="toggle-icon">{{ item.isOpen ? '−' : '+' }}</span>
              </button>
              <div class="faq-answer" v-show="item.isOpen">
                <p>{{ item.answer }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="contact-section">
        <div class="glass-card contact-card">
          <h2 class="serif-title">Receba nossas <span class="gold-text">novidades</span></h2>
          <p>Assine nossa newsletter para dicas exclusivas de beleza e promoções do salão.</p>

          <form @submit.prevent="handleLeadSubmit" class="lead-form" novalidate>
            <div class="form-group">
              <input 
                type="email" 
                v-model="leadEmail" 
                @blur="touched = true"
                placeholder="Seu melhor e-mail" 
                required 
                :class="{ 'input-error': emailErrorMsg }"
              />
              <span v-if="emailErrorMsg" class="error-msg" role="alert">{{ emailErrorMsg }}</span>
            </div>

            <button 
              type="submit" 
              class="btn primary-gold large" 
              :disabled="!isEmailValid || isSubmitting"
            >
              <span v-if="isSubmitting">Inscrevendo...</span>
              <span v-else-if="submitSuccess">Inscrito com sucesso! ✓</span>
              <span v-else>Assinar Newsletter</span>
            </button>
          </form>
        </div>
      </section>

    </main>
  </div>
</template>

<style scoped>
/* ==========================================
 * DESIGN SYSTEM: Dark & Gold High-End
 * Tipografia elegante e paleta Preto/Dourado
 * ========================================== */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

.landing-page {
  background-color: #050505; /* Fundo base escuro */
  color: #fff;
  font-family: 'Inter', sans-serif;
  min-height: 100vh;
  scroll-behavior: smooth;
  /* Brilho dourado de fundo bem suave para criar atmosfera premium */
  background-image: radial-gradient(circle at 50% -10%, rgba(212, 175, 55, 0.08) 0%, transparent 60%);
}

.serif-title {
  font-family: 'Playfair Display', serif;
  font-weight: 400;
  letter-spacing: -0.5px;
  line-height: 1.1;
}

.gold-text {
  background: linear-gradient(135deg, #d4af37, #f1c40f);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* HEURÍSTICA 1: Progress Bar Vertical (Esquerda) */
.scroll-progress-bar {
  position: fixed; 
  top: 0; 
  left: 0; 
  width: 3px; 
  background: linear-gradient(180deg, #d4af37, #f1c40f);
  z-index: 1000; 
  transition: height 0.1s ease-out; 
}

/* ==========================================
 * HEADER STICKY
 * ========================================== */
.sticky-nav {
  position: fixed; top: 0; width: 100%;
  background: rgba(5, 5, 5, 0.9);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  z-index: 999; padding: 16px 5%;
}

.nav-content {
  max-width: 1400px; margin: 0 auto;
  display: flex; justify-content: space-between; align-items: center;
}

.logo { font-family: 'Playfair Display', serif; font-size: 26px; font-weight: 600; }
.logo span { font-weight: 400; }

.nav-links { display: flex; gap: 40px; text-transform: uppercase; letter-spacing: 1px; font-size: 12px; }
.nav-links a { color: #aaa; text-decoration: none; transition: color 0.3s; }
.nav-links a:hover { color: #d4af37; }

.content-wrapper { max-width: 1400px; margin: 0 auto; padding: 120px 5% 60px; display: flex; flex-direction: column; gap: 100px; }

/* ==========================================
 * GLASSMORPHISM CARD SYSTEM (Layout 100% em Cards)
 * ========================================== */
.glass-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 4px; /* Linhas mais retas para ar editorial */
  backdrop-filter: blur(20px);
  box-shadow: 0 40px 80px rgba(0,0,0,0.5);
  overflow: hidden;
  transition: border-color 0.4s ease, box-shadow 0.4s ease;
}

/* ==========================================
 * COMPONENTES DE TEXTO E BOTÕES
 * ========================================== */
.eyebrow { font-size: 11px; letter-spacing: 5px; text-transform: uppercase; color: #d4af37; margin-bottom: 16px; display: block; }
h1.serif-title { font-size: clamp(48px, 4.5vw, 72px); margin-bottom: 24px; }
h2.serif-title { font-size: clamp(36px, 4vw, 48px); margin-bottom: 24px; }
h3.serif-title.small { font-size: 24px; margin-bottom: 12px; }

p { color: #999; line-height: 1.6; font-size: 15px; font-weight: 300; }

.center { text-align: center; margin-bottom: 60px; }

/* LEI DE FITTS: Botões generosos */
.btn {
  display: inline-flex; justify-content: center; align-items: center;
  padding: 14px 32px; font-weight: 600; text-decoration: none; cursor: pointer;
  transition: all 0.3s ease; border: none; font-family: inherit; min-height: 48px;
  letter-spacing: 0.5px; border-radius: 4px;
}

/* Botão Ouro Principal */
.btn.primary-gold { background: linear-gradient(135deg, #d4af37, #f1c40f); color: #000; }
.btn.primary-gold:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(212, 175, 55, 0.3); }
.btn.primary-gold:disabled { opacity: 0.5; cursor: not-allowed; }

/* Botão Contorno Ouro */
.btn.outline-gold { background: transparent; color: #d4af37; border: 1px solid rgba(212,175,55,0.4); }
.btn.outline-gold:hover { border-color: #d4af37; background: rgba(212,175,55,0.05); }

/* Botão Secundário Sutil */
.btn.ghost-gold { background: transparent; color: #aaa; padding: 10px 0; min-height: auto; justify-content: flex-start; }
.btn.ghost-gold:hover { color: #d4af37; }

.btn.large { padding: 18px 40px; font-size: 16px; }

/* ==========================================
 * HERO & SOBRE NÓS (DUAL CARDS)
 * ========================================== */
 
.dual-card { display: grid; grid-template-columns: 1fr 1fr; min-height: 500px; }
.dual-card.flipped { grid-template-columns: 1fr 1fr; }
.dual-content { padding: 80px; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; }
.dual-content p { margin-bottom: 40px; font-size: 18px; max-width: 450px; }

/* Placeholders para Imagens */
.dual-image { background: #0a0a0a; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; border: 1px solid rgba(255,255,255,0.02); }
.image-label { color: #444; font-size: 13px; text-transform: uppercase; letter-spacing: 2px; }
.image-placeholder-1 {
   background: radial-gradient(circle, #111, #080808);
   background-image: url('https://images.pexels.com/photos/16985916/pexels-photo-16985916.jpeg?auto=compress&cs=tinysrgb&w=800');
   background-size: cover;
   }
.image-placeholder-2 {
   background: radial-gradient(circle, #080808, #111);
   background-image: url('https://images.pexels.com/photos/7446910/pexels-photo-7446910.jpeg?auto=compress&cs=tinysrgb&w=800');
   background-size: cover;
   }

/* ==========================================
 * SERVIÇOS (HOVER EFFECTS)
 * ========================================== */
.features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 32px; }
.service-card { padding: 40px; display: flex; flex-direction: column; align-items: flex-start; transition: transform 0.4s ease, border-color 0.4s ease; }
.service-card:hover { transform: translateY(-8px); border-color: rgba(212, 175, 55, 0.4); box-shadow: 0 20px 40px rgba(0,0,0,0.5), 0 0 40px rgba(212,175,55,0.05); }
.service-card.featured { border-color: rgba(212, 175, 55, 0.2); }

.card-img { 
  width: 100%; height: 220px; background: rgba(255,255,255,0.03); margin-bottom: 24px; border-radius: 2px; 
  background-size: cover !important;
  background-position: center !important;
  background-repeat: no-repeat !important;
}
.placeholder-corte { background-image: url('https://images.pexels.com/photos/15659458/pexels-photo-15659458.jpeg?auto=compress&cs=tinysrgb&w=800'); }
.placeholder-cor   { background-image: url('https://images.pexels.com/photos/19192425/pexels-photo-19192425.jpeg?auto=compress&cs=tinysrgb&w=800'); }
.placeholder-unhas { background-image: url('https://images.pexels.com/photos/37033378/pexels-photo-37033378.jpeg?auto=compress&cs=tinysrgb&w=800'); }
.service-card p { margin-bottom: 24px; flex-grow: 1; }

/* ==========================================
 * FAQ
 * ========================================== */
 .faq-question .serif-title {
  font-size: 20px; 
}
.faq-answer p {
  font-size: 14px; 
}
.faq-container { padding: 60px; max-width: 800px; margin: 0 auto; width: 100%; text-align: center; }
.faq-list { margin-top: 40px; display: flex; flex-direction: column; gap: 16px; text-align: left; }
.faq-item { border-bottom: 1px solid rgba(255,255,255,0.1); overflow: hidden; transition: all 0.3s; }
.faq-item.open { border-color: rgba(212, 175, 55, 0.4); }
.faq-question { width: 100%; display: flex; justify-content: space-between; align-items: center; padding: 24px 0; background: none; border: none; color: #fff; cursor: pointer; }
.toggle-icon { font-size: 24px; transition: transform 0.3s; font-weight: 300; color: #d4af37; }
.faq-item.open .toggle-icon { transform: rotate(180deg); }
.faq-answer { padding: 0 0 24px 0; color: #aaa; }

/* ==========================================
 * CONTATO / NEWSLETTER
 * ========================================== */
.contact-card { max-width: 600px; margin: 0 auto; width: 100%; text-align: center; padding: 80px 40px; border-color: rgba(212, 175, 55, 0.15); }
.contact-card p { margin-bottom: 40px; }
.lead-form { display: flex; flex-direction: column; gap: 16px; }
.form-group input { width: 100%; padding: 16px 20px; border: 1px solid rgba(255,255,255,0.15); background: rgba(0,0,0,0.3); color: #fff; font-family: inherit; font-size: 16px; outline: none; transition: border-color 0.3s; border-radius: 4px;}
.form-group input:focus { border-color: #d4af37; }
.form-group input.input-error { border-color: #e74c3c; background: rgba(231, 76, 60, 0.05); }
.error-msg { color: #e74c3c; font-size: 13px; display: block; text-align: left; margin-top: 8px; }

/* Responsividade */
@media (max-width: 960px) {
  .nav-links { display: none; /* Lei de Hick: Simplifica mobile */ }
  .dual-card, .dual-card.flipped { grid-template-columns: 1fr; }
  .dual-image { min-height: 300px; }
  .dual-content { padding: 40px 20px; text-align: center; align-items: center; }
  .content-wrapper { padding-top: 100px; gap: 60px; }
  .hero-actions { justify-content: center; }
}
</style>