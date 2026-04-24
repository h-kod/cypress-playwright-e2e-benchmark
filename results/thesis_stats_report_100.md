# Ölçüm Ortamı

- Playwright ölçümü: results/playwright/playwright_benchmark_100.csv
- Cypress ölçümü: results/cypress/cypress_benchmark_100.csv
- Özet CSV: results/summaries/benchmark_summary_100.csv
- Playwright konfigürasyonu headless modda 1 worker ile çalışacak şekilde ayarlı.
- Cypress, Electron tarayıcısı ile headless modda çalıştırılmış.
- Tekrar sayısı: 100

# Kullanılan Komutlar

- `npm run test:playwright`
- `npm run test:cypress`
- `python scripts/benchmark.py --tool playwright --command "npm run test:playwright" --repeat 100 --output results/playwright/playwright_benchmark_100.csv`
- `python scripts/benchmark.py --tool cypress --command "npm run test:cypress" --repeat 100 --output results/cypress/cypress_benchmark_100.csv`
- `python scripts/summarize_results.py --playwright results/playwright/playwright_benchmark_100.csv --cypress results/cypress/cypress_benchmark_100.csv --output results/summaries/benchmark_summary_100.csv`

# Süre Analizi Özeti

- Playwright ortalama süre: 3,7790 sn
- Cypress ortalama süre: 13,7650 sn
- Mutlak fark: 9,9860 sn
- Göreli fark: 264,2498 %

## CPU Analizi

### Playwright
- Ortalama: 114,4989
- Medyan: 114,6647
- Standart sapma: 6,5136
- Minimum: 100,5859
- Maksimum: 128,9062
### Cypress
- Ortalama: 141,8972
- Medyan: 141,4931
- Standart sapma: 4,2953
- Minimum: 132,5721
- Maksimum: 155,4087
### Normallik
- Playwright Shapiro-Wilk: W = 0,9812, p = 0,1645
- Cypress Shapiro-Wilk: W = 0,9686, p = 0,0173
### Grup Karşılaştırması
- Mann-Whitney U: U = 0,0000, p = < 0,0001
- Etki büyüklüğü: rank-biserial correlation = -1,0000
- Cliff's delta: -1,0000
- Welch t-testi: t = -35,1155, p = < 0,0001
- Cohen's d: -4,9661
### Kısa Yorum
- Playwright bu metrikte daha düşük değer göstermiştir. Mann-Whitney U testi sonuçları iki araç arasında istatistiksel olarak anlamlı fark olduğunu göstermektedir.

## Ortalama RAM Analizi

### Playwright
- Ortalama: 347,2740
- Medyan: 347,8349
- Standart sapma: 9,4250
- Minimum: 321,6326
- Maksimum: 367,7836
### Cypress
- Ortalama: 923,5276
- Medyan: 922,7743
- Standart sapma: 9,4749
- Minimum: 907,4439
- Maksimum: 993,2221
### Normallik
- Playwright Shapiro-Wilk: W = 0,9749, p = 0,0531
- Cypress Shapiro-Wilk: W = 0,7138, p = < 0,0001
### Grup Karşılaştırması
- Mann-Whitney U: U = 0,0000, p = < 0,0001
- Etki büyüklüğü: rank-biserial correlation = -1,0000
- Cliff's delta: -1,0000
- Welch t-testi: t = -431,1890, p = < 0,0001
- Cohen's d: -60,9793
### Kısa Yorum
- Playwright bu metrikte daha düşük değer göstermiştir. Mann-Whitney U testi sonuçları iki araç arasında istatistiksel olarak anlamlı fark olduğunu göstermektedir.

## Tepe RAM Analizi

### Playwright
- Ortalama: 675,8011
- Medyan: 675,5332
- Standart sapma: 15,2885
- Minimum: 638,6367
- Maksimum: 701,1523
### Cypress
- Ortalama: 1264,9963
- Medyan: 1261,9668
- Standart sapma: 24,8697
- Minimum: 1246,8672
- Maksimum: 1506,2227
### Normallik
- Playwright Shapiro-Wilk: W = 0,9726, p = 0,0350
- Cypress Shapiro-Wilk: W = 0,2068, p = < 0,0001
### Grup Karşılaştırması
- Mann-Whitney U: U = 0,0000, p = < 0,0001
- Etki büyüklüğü: rank-biserial correlation = -1,0000
- Cliff's delta: -1,0000
- Welch t-testi: t = -201,8266, p = < 0,0001
- Cohen's d: -28,5426
### Kısa Yorum
- Playwright bu metrikte daha düşük değer göstermiştir. Mann-Whitney U testi sonuçları iki araç arasında istatistiksel olarak anlamlı fark olduğunu göstermektedir.

# Başarı Durumu

- Playwright başarı toplamı: 100 / 100
- Cypress başarı toplamı: 100 / 100
- Başarısız koşum bulunamadı.

# İstatistiksel Yöntem Gerekçesi

- Ham veri setleri 100 tekrar içerir; normallik Shapiro-Wilk testi ile kontrol edilmiştir.
- CPU için Cypress tarafında tüm değerler 0 olduğundan normallik varsayımı sağlanmaz; bu yüzden Mann-Whitney U testi daha uygundur.
- RAM metriklerinde de normal dağılımın desteklenmediği durumda non-parametrik test ana sonuç olarak, Welch t-testi ise tamamlayıcı kontrol olarak raporlanmıştır.

# Teze Yazılabilecek Sonuç Paragrafı

Bu benchmark çalışmasında Playwright ve Cypress, aynı demo kullanıcı akışı 100 tekrar üzerinden karşılaştırılmıştır. Playwright tarafı headless modda tek worker ile, Cypress tarafı ise headless Electron tarayıcısı üzerinden çalıştırılmıştır. Sonuçlar, CPU kullanımında Cypress'in ölçüm boyunca 0,0000 değerinde kalması nedeniyle dağılımın normal olmadığını ve farkın non-parametrik testlerle değerlendirilmesi gerektiğini göstermiştir. Hem ortalama RAM hem de tepe RAM metriklerinde Playwright, Cypress'e göre daha düşük kaynak tüketmiştir. Mann-Whitney U ve Welch t-testi sonuçları metrikler arasında istatistiksel olarak anlamlı fark bulunduğunu desteklemekte, etki büyüklüğü ise farkın güçlü olduğunu göstermektedir.

# Ekler İçin Önerilen Kod Parçaları

- Ek-1: Benchmark ölçüm betiği önemli bölümü
  - Dosya yolu: `scripts/benchmark.py`
  - Satır aralığı: 57-89 ve 127-144
  - Neden önemli: Ham CSV'lerin nasıl üretildiğini, CPU/RAM ölçümünün nasıl örneklendiğini ve tekrar mantığını gösterir.
  - Teze konulacak kısa açıklama: Tekrarlı benchmark ölçüm mekanizması ve metrik toplama yaklaşımı.
- Ek-2: Playwright test senaryosu önemli bölümü
  - Dosya yolu: `playwright-tests/e2e.spec.js`
  - Satır aralığı: 3-36
  - Neden önemli: Karşılaştırılan kullanıcı akışını ve doğrulama adımlarını gösterir.
  - Teze konulacak kısa açıklama: Aynı akışın Playwright ile uçtan uca test tanımı.
- Ek-3: Cypress test senaryosu önemli bölümü
  - Dosya yolu: `cypress/e2e/app.cy.js`
  - Satır aralığı: 1-36
  - Neden önemli: Playwright ile aynı akışın Cypress tarafındaki eşdeğerini gösterir.
  - Teze konulacak kısa açıklama: Aynı iş akışının Cypress ile eşdeğer test implementasyonu.
- Ek-4: Çalıştırma komutları
  - Dosya yolu: `package.json`, `scripts/run-cypress.js`, `playwright.config.js`
  - Satır aralığı: `package.json` 6-9, `scripts/run-cypress.js` 1-11, `playwright.config.js` 1-12
  - Neden önemli: Çalıştırma modunu, headless ayarını ve kullanılan komutları açıkça gösterir.
  - Teze konulacak kısa açıklama: Benchmark'ın hangi komutlarla ve hangi çalışma modunda yürütüldüğü.
- Ek-5: CSV çıktı örneği
  - Dosya yolu: `results/playwright/playwright_benchmark_100.csv`, `results/cypress/cypress_benchmark_100.csv`, `results/summaries/benchmark_summary_100.csv`
  - Satır aralığı: her dosyada ilk 2-6 satır
  - Neden önemli: Ham ölçümlerin ve özet istatistiklerin tezde şeffaf biçimde sunulmasını sağlar.
  - Teze konulacak kısa açıklama: Benchmark'ın sayısal çıktıları ve özetleme formatı.
