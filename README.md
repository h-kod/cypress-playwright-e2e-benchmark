# Cypress vs Playwright E2E Benchmark

Bu depo, aynÄ± demo uygulama Ã¼zerinde **Cypress** ve **Playwright** ile yazÄ±lmÄ±ÅŸ uÃ§tan uca testlerin performansÄ±nÄ± karÅŸÄ±laÅŸtÄ±rmak iÃ§in hazÄ±rlanmÄ±ÅŸ bir benchmark Ã§alÄ±ÅŸmasÄ±dÄ±r.

Ã‡alÄ±ÅŸmanÄ±n ana odaÄŸÄ± sadece testlerin "geÃ§mesi" deÄŸildir. AsÄ±l amaÃ§, iki aracÄ±n aynÄ± kullanÄ±cÄ± akÄ±ÅŸlarÄ±nda:

- Ã§alÄ±ÅŸma sÃ¼resi
- bellek tÃ¼ketimi
- tekrarlar arasÄ±ndaki kararlÄ±lÄ±k
- Ã¶lÃ§Ã¼m Ã§Ä±ktÄ±larÄ±nÄ±n raporlanabilirliÄŸi

gibi boyutlarda nasÄ±l davrandÄ±ÄŸÄ±nÄ± gÃ¶rÃ¼nÃ¼r hale getirmektir.

## KÄ±sa Ã–zet

Projede Ã¼Ã§ temel kullanÄ±cÄ± akÄ±ÅŸÄ±, baseline iÅŸlevsel kullanÄ±cÄ± akÄ±ÅŸÄ± kapsamÄ±nda test edilir:

1. giriÅŸ yapma
2. Ã¼rÃ¼nÃ¼ sepete ekleme
3. sipariÅŸi tamamlama

Bu baseline akÄ±ÅŸ hem Cypress hem de Playwright tarafÄ±nda eÅŸdeÄŸer ÅŸekilde koÅŸturulur. ArdÄ±ndan 100 tekrar Ã¼zerinden Ã¶lÃ§Ã¼m alÄ±nÄ±r ve CSV raporlarÄ±na yazÄ±lÄ±r.

Benchmark Ã¶zetine gÃ¶re:

| AraÃ§ | BaÅŸarÄ±lÄ± Ã‡alÄ±ÅŸma | Ortalama SÃ¼re | Ortalama CPU | Ortalama Bellek | Tepe Bellek |
|---|---:|---:|---:|---:|---:|
| Playwright | 100 / 100 | 4.0135 sn | 107.7352 % | 373.7757 MB | 739.8229 MB |
| Cypress | 100 / 100 | 13.8553 sn | 143.7743 % | 957.4314 MB | 1333.6548 MB |

Bu sonuÃ§lar, bu projedeki demo senaryosu Ã¶zelinde Playwrightâ€™Ä±n daha hÄ±zlÄ± ve daha hafif Ã§alÄ±ÅŸtÄ±ÄŸÄ±nÄ± gÃ¶sterir.

## Ölçüm Ortamı

- İşletim sistemi: Windows
- Node.js: v25.9.0
- Playwright: headless mod, 1 worker
- Cypress: headless Electron
- Tekrar sayısı: profil başına 100

## Sonuç Paketi

Son benchmark ve analiz çıktıları `results/` altında profil bazlı düzenlenir:

- `results/playwright/baseline_benchmark_100.csv`
- `results/playwright/ui-heavy_benchmark_100.csv`
- `results/playwright/cpu-heavy_benchmark_100.csv`
- `results/playwright/ram-heavy_benchmark_100.csv`
- `results/cypress/baseline_benchmark_100.csv`
- `results/cypress/ui-heavy_benchmark_100.csv`
- `results/cypress/cpu-heavy_benchmark_100.csv`
- `results/cypress/ram-heavy_benchmark_100.csv`
- `results/summaries/profile_metric_summary.csv`
- `results/summaries/profile_comparison_stats.csv`
- `results/profile_thesis_report_100.md`
- `results/graphs/`

Bu paket, tez tablosuna aktarılacak değerlerin virgüllü ondalık biçime dönüştürülmesine uygun özetleri de içerir.

## Komutlar

Profil bazlı test ve benchmark komutları:

- `npm run test:playwright:baseline`
- `npm run test:playwright:ui-heavy`
- `npm run test:playwright:cpu-heavy`
- `npm run test:playwright:ram-heavy`
- `npm run test:cypress:baseline`
- `npm run test:cypress:ui-heavy`
- `npm run test:cypress:cpu-heavy`
- `npm run test:cypress:ram-heavy`
- `npm run benchmark:all`
- `npm run analyze:profiles`
## Repo YapÄ±sÄ±

```text
app/                Demo uygulamanÄ±n HTML sayfasÄ±
cypress/            Cypress testleri
playwright-tests/   Playwright testleri
scripts/            Benchmark ve raporlama scriptleri
results/            CSV sonuÃ§larÄ± ve Ã¶zetler
docs/               Ã‡alÄ±ÅŸma notlarÄ±, loglar ve baÅŸarÄ± ekran gÃ¶rÃ¼ntÃ¼leri
screenshots/        Test akÄ±ÅŸÄ±na ait gÃ¶rseller ve benchmark Ã§Ä±ktÄ±larÄ±
```

## Demo Uygulama

Testlerin Ã§alÄ±ÅŸtÄ±ÄŸÄ± Ã¶rnek uygulama `app/index.html` iÃ§inde yer alÄ±r. Uygulama, benchmark iÃ§in Ã¶zellikle basit tutulmuÅŸtur ve ÅŸu etkileÅŸimleri iÃ§erir:

- kullanÄ±cÄ± adÄ± ve parola ile giriÅŸ
- Ã¼rÃ¼n kartlarÄ± Ã¼zerinden sepete Ã¼rÃ¼n ekleme
- sipariÅŸ formu doldurma
- sipariÅŸi tamamlama mesajÄ±nÄ± doÄŸrulama

Bu sade akÄ±ÅŸ, iki test aracÄ±nÄ± aynÄ± koÅŸullarda karÅŸÄ±laÅŸtÄ±rmayÄ± kolaylaÅŸtÄ±rÄ±r.

## Test AkÄ±ÅŸÄ±

Bu depoda korunan baseline testler ÅŸunlardÄ±r:

- baÅŸarÄ±lÄ± sipariÅŸ akÄ±ÅŸÄ±
- geÃ§ersiz giriÅŸ
- boÅŸ sepetle sipariÅŸ

BaÅŸarÄ±lÄ± sipariÅŸ akÄ±ÅŸÄ±nda sÄ±rasÄ±yla ÅŸu davranÄ±ÅŸlar doÄŸrulanÄ±r:

1. Demo uygulama aÃ§Ä±lÄ±r.
2. KullanÄ±cÄ± bilgileri ile giriÅŸ yapÄ±lÄ±r.
3. ÃœrÃ¼nler arasÄ±ndan bir Ã¶ÄŸe sepete eklenir.
4. SipariÅŸ formu doldurulur.
5. SipariÅŸin baÅŸarÄ±yla tamamlandÄ±ÄŸÄ± mesajÄ± kontrol edilir.

`docs/test-log.md` iÃ§indeki notlara gÃ¶re baseline akÄ±ÅŸÄ± ve profil testleri her iki framework tarafÄ±nda da baÅŸarÄ±lÄ± ÅŸekilde geÃ§mektedir.

Ek olarak demo uygulamada ÅŸu profil testleri bulunur:

- UI-heavy profil testi
- CPU-heavy profil testi
- RAM-heavy profil testi

## GÃ¶rsel KanÄ±tlar

### Demo Uygulama EkranlarÄ±

`screenshots/demoapp1.png`

![GiriÅŸ ekranÄ±](screenshots/demoapp1.png)

`screenshots/demoapp2.png`

![ÃœrÃ¼n ekleme ve sipariÅŸ formu](screenshots/demoapp2.png)

`screenshots/demoapp3.png`

![SipariÅŸin baÅŸarÄ±yla tamamlanmasÄ±](screenshots/demoapp3.png)

Bu Ã¼Ã§ gÃ¶rÃ¼ntÃ¼, testin uÃ§tan uca iÅŸ akÄ±ÅŸÄ±nÄ± belgeliyor:

- ilk gÃ¶rsel giriÅŸ ekranÄ±nÄ±
- ikinci gÃ¶rsel sepete Ã¼rÃ¼n eklenmesi ve form alanlarÄ±nÄ±
- Ã¼Ã§Ã¼ncÃ¼ gÃ¶rsel ise baÅŸarÄ± mesajÄ± ile tamamlanan sipariÅŸ durumunu
 
### Ek GÃ¶rseller

`screenshots/cypress050.jpg`

![Cypress 0.50 gÃ¶rÃ¼ntÃ¼sÃ¼](screenshots/cypress050.jpg)

`screenshots/cypress50100.jpg`

![Cypress 50/100 gÃ¶rÃ¼ntÃ¼sÃ¼](screenshots/cypress50100.jpg)

`screenshots/playwright050.jpg`

![Playwright 0.50 gÃ¶rÃ¼ntÃ¼sÃ¼](screenshots/playwright050.jpg)

`screenshots/playwright50100.jpg`

![Playwright 50/100 gÃ¶rÃ¼ntÃ¼sÃ¼](screenshots/playwright50100.jpg)

### Benchmark Ã‡Ä±ktÄ±larÄ±

Bu bÃ¶lÃ¼mdeki referanslar, geÃ§miÅŸ benchmark Ã§Ä±ktÄ±larÄ±nÄ±n nasÄ±l arÅŸivlendiÄŸini gÃ¶sterir. GÃ¼ncel benchmark sonuÃ§larÄ± 100 tekrar Ã¼zerinden Ã¼retilmiÅŸtir ve esas alÄ±nmasÄ± gereken CSV dosyalar `results/` altÄ±ndadÄ±r.

## SonuÃ§ DosyalarÄ±

`results/` klasÃ¶rÃ¼ benchmark Ã§Ä±ktÄ±larÄ±nÄ±n toplandÄ±ÄŸÄ± yerdir.

- `results/playwright/playwright_benchmark_100.csv`: Playwright iÃ§in ham tekrar Ã¶lÃ§Ã¼mleri
- `results/cypress/cypress_benchmark_100.csv`: Cypress iÃ§in ham tekrar Ã¶lÃ§Ã¼mleri
- `results/summaries/benchmark_summary_100.csv`: iki aracÄ±n karÅŸÄ±laÅŸtÄ±rmalÄ± Ã¶zeti
- `results/thesis_stats_report_100.md`: tez iÃ§in hazÄ±rlanmÄ±ÅŸ analiz raporu
- `results/playwright/baseline_benchmark_100.csv`: baseline ham ölçümleri
- `results/playwright/ui-heavy_benchmark_100.csv`: UI-heavy ham ölçümleri
- `results/playwright/cpu-heavy_benchmark_100.csv`: CPU-heavy ham ölçümleri
- `results/playwright/ram-heavy_benchmark_100.csv`: RAM-heavy ham ölçümleri
- `results/cypress/baseline_benchmark_100.csv`: baseline ham ölçümleri
- `results/cypress/ui-heavy_benchmark_100.csv`: UI-heavy ham ölçümleri
- `results/cypress/cpu-heavy_benchmark_100.csv`: CPU-heavy ham ölçümleri
- `results/cypress/ram-heavy_benchmark_100.csv`: RAM-heavy ham ölçümleri
- `results/summaries/profile_metric_summary.csv`: tool/profile/metric bazlı genel özet
- `results/summaries/profile_comparison_stats.csv`: profil bazlı karşılaştırma istatistikleri
- `results/profile_thesis_report_100.md`: profil bazlı tez raporu
- `results/graphs/`: profil ve metrik bazlı grafikler

Ã–zet CSVâ€™den gÃ¶rÃ¼len temel metrikler:

- Playwright: 100/100 baÅŸarÄ±lÄ±, ortalama sÃ¼re 4.0135 sn, ortalama CPU 107.7352 %, ortalama bellek 373.7757 MB
- Cypress: 100/100 baÅŸarÄ±lÄ±, ortalama sÃ¼re 13.8553 sn, ortalama CPU 143.7743 %, ortalama bellek 957.4314 MB

## Profil LaboratuvarÄ±

Demo uygulamada baseline iÅŸlevsel kullanÄ±cÄ± akÄ±ÅŸÄ±ndan ayrÄ± olarak Ã¼Ã§ profil alanÄ± bulunur:

- UI-heavy profil yapÄ±sÄ±
- CPU-heavy profil yapÄ±sÄ±
- RAM-heavy profil yapÄ±sÄ±

Bu profiller test edilebilir `data-testid` seÃ§icileri ile birlikte gelir ve baseline benchmark sonuÃ§larÄ±nÄ± deÄŸiÅŸtirmez. GÃ¼ncel CSV Ã¶zetleri hÃ¢lÃ¢ yalnÄ±zca baseline iÅŸlevsel kullanÄ±cÄ± akÄ±ÅŸÄ± iÃ§in geÃ§erlidir.

## Loglar ve Raporlar

`docs/` klasÃ¶rÃ¼, Ã§alÄ±ÅŸmanÄ±n okunmasÄ±nÄ± kolaylaÅŸtÄ±ran destek dosyalarÄ±nÄ± iÃ§erir:

- `docs/cypress-test-output.txt`: Cypress test Ã§Ä±ktÄ±sÄ±
- `docs/playwright-test-output.txt`: Playwright test Ã§Ä±ktÄ±sÄ±
- `docs/cypress-benchmark-100.log`: Cypress benchmark kayÄ±tlarÄ±
- `docs/playwright-benchmark-100.log`: Playwright benchmark kayÄ±tlarÄ±
- `docs/test-log.md`: Ã§alÄ±ÅŸmanÄ±n kÄ±sa operasyonel Ã¶zeti

Bu dosyalar, yalnÄ±zca sonuÃ§larÄ± deÄŸil, sonucun nasÄ±l oluÅŸtuÄŸunu da takip etmeyi kolaylaÅŸtÄ±rÄ±r.

## Kurulum

Projeyi Ã§alÄ±ÅŸtÄ±rmak iÃ§in Node.js tabanlÄ± baÄŸÄ±mlÄ±lÄ±klarÄ±n kurulmasÄ± gerekir:

```bash
npm install
```

Playwright tarafÄ±nda tarayÄ±cÄ±larÄ±n ayrÄ±ca kurulmasÄ± gerekiyorsa:

```bash
npx playwright install
```

## Ã‡alÄ±ÅŸtÄ±rma

### Playwright testi

```bash
npm run test:playwright
```

### Cypress testi

```bash
npm run test:cypress
```

### Profil BazlÄ± Test KomutlarÄ±

Playwright:

```bash
npm run test:playwright:baseline
npm run test:playwright:ui-heavy
npm run test:playwright:cpu-heavy
npm run test:playwright:ram-heavy
```

Cypress:

```bash
npm run test:cypress:baseline
npm run test:cypress:ui-heavy
npm run test:cypress:cpu-heavy
npm run test:cypress:ram-heavy
```

## Benchmark Ãœretimi

Benchmark ve Ã¶zet raporlar `scripts/` klasÃ¶rÃ¼ndeki Python scriptleri ile Ã¼retilir:

- `scripts/benchmark.py`
- `scripts/summarize_results.py`
- `scripts/run-cypress.js`
- `scripts/analyze_stats_for_thesis.py`

Profil bazlÄ± Ã¶zet, karÅŸÄ±laÅŸtÄ±rma ve grafik Ã¼retimi iÃ§in:

```bash
npm run analyze:profiles
```

Bu analiz, `results/{tool}/{profile}_benchmark_100.csv` dosyalarÄ±nÄ± okuyarak `results/summaries/profile_metric_summary.csv`, `results/summaries/profile_comparison_stats.csv` ve `results/graphs/` altÄ±nda profil bazlÄ± Ã§Ä±ktÄ±lar Ã¼retir.

Profil bazlÄ± benchmark koÅŸularÄ±nÄ± tek seferde Ã¼retmek iÃ§in:

```bash
npm run benchmark:all
```

Bu komut, Playwright ve Cypress iÃ§in `baseline`, `ui-heavy`, `cpu-heavy` ve `ram-heavy` profillerinin tamamÄ±nÄ± 100 tekrar Ã§alÄ±ÅŸtÄ±rÄ±r ve Ã§Ä±ktÄ±larÄ± `results/{tool}/{profile}_benchmark_100.csv` biÃ§iminde yazar.

Ã–zet oluÅŸturma mantÄ±ÄŸÄ±, ham CSV dosyalarÄ±nÄ± okuyup baÅŸarÄ± sayÄ±sÄ±, sÃ¼re ortalamasÄ±, CPU ortalamasÄ± ve bellek istatistiklerini tek bir karÅŸÄ±laÅŸtÄ±rma tablosuna dÃ¶nÃ¼ÅŸtÃ¼rmektir.

## Raporun YorumlanmasÄ±

Bu Ã§alÄ±ÅŸmada iki noktaya Ã¶zellikle dikkat etmek gerekir:

1. **BaÅŸarÄ± oranÄ± eÅŸit**: Her iki araÃ§ da 100 denemenin 100â€™Ã¼nÃ¼ baÅŸarÄ±yla tamamlamÄ±ÅŸtÄ±r.
2. **Kaynak kullanÄ±mÄ± farklÄ±**: AynÄ± akÄ±ÅŸta Cypress, Playwrightâ€™a gÃ¶re daha uzun sÃ¼rmÃ¼ÅŸ ve daha fazla bellek tÃ¼ketmiÅŸtir.

Bu nedenle bu depo, yalnÄ±zca "hangi araÃ§ daha hÄ±zlÄ±" sorusuna deÄŸil, aynÄ± zamanda "aynÄ± kullanÄ±cÄ± akÄ±ÅŸÄ±nda hangi araÃ§ daha verimli raporlanÄ±yor" sorusuna da veri saÄŸlar.

## Not

Buradaki sonuÃ§lar bu depo iÃ§indeki demo uygulama, test senaryolarÄ± ve Ã¶lÃ§Ã¼m yÃ¶ntemi iÃ§in geÃ§erlidir. GerÃ§ek projelerde uygulama karmaÅŸÄ±klÄ±ÄŸÄ±, aÄŸ gecikmesi, fixture yapÄ±sÄ± ve test mimarisi bu deÄŸerleri ciddi biÃ§imde deÄŸiÅŸtirebilir.





