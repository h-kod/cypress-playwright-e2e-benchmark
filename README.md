# Cypress Playwright E2E Benchmark

Cypress ve Playwright çerçevelerinin uçtan uca test senaryolarında performans, süre ve kaynak tüketimi açısından karşılaştırılmasını amaçlayan benchmark projesidir.

## Amaç
Bu projede, eşdeğer E2E test senaryoları altında Cypress ve Playwright araçlarının:
- toplam test süresi
- CPU kullanımı
- RAM tüketimi
- tekrarlar arasındaki tutarlılığı

karşılaştırılacaktır.

## Kapsam
Projede örnek bir web uygulaması üzerinde giriş yapma, sepete ürün ekleme ve form doldurma gibi temel kullanıcı akışları test edilecektir. Testler otomatik olarak çalıştırılacak ve ölçüm verileri Python tabanlı scriptlerle toplanacaktır.

## Çıktılar
- Playwright test senaryoları
- Cypress test senaryoları
- Benchmark ölçüm scriptleri
- CSV sonuç dosyaları
- Grafikler ve özet rapor
