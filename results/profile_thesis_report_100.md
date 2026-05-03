# Profil Bazl? Sonu? Raporu

## ?l??m Ortam?
- ?al??ma sistemi: Windows
- Node.js: v25.9.0
- Playwright testleri headless ve 1 worker ile ?al??t?r?ld?.
- Cypress testleri headless Electron taray?c?s? ile ?al??t?r?ld?.
- Her kombinasyon 100 tekrar ?zerinden ?l??ld?.

## Ba?ar? ?zeti
| Tool | Profile | Success | Failure | Rate (%) |
|---|---|---:|---:|---:|
| playwright | baseline | 100 | 0 | 100,0000 |
| playwright | ui-heavy | 100 | 0 | 100,0000 |
| playwright | cpu-heavy | 100 | 0 | 100,0000 |
| playwright | ram-heavy | 100 | 0 | 100,0000 |
| cypress | baseline | 100 | 0 | 100,0000 |
| cypress | ui-heavy | 100 | 0 | 100,0000 |
| cypress | cpu-heavy | 100 | 0 | 100,0000 |
| cypress | ram-heavy | 100 | 0 | 100,0000 |

## Genel Summary
| Tool | Profile | S?re | Ortalama CPU | Ortalama Sistem CPU | Ortalama Bellek | Tepe Bellek | CPU S?resi |
|---|---|---:|---:|---:|---:|---:|---:|
| playwright | baseline | 4,0135 | 107,7352 | 39,8930 | 373,7757 | 739,8229 | 3,8709 |
| playwright | ui-heavy | 3,4292 | 111,3782 | 37,6910 | 316,3226 | 706,2265 | 3,3911 |
| playwright | cpu-heavy | 3,3655 | 109,7913 | 34,7155 | 315,3874 | 702,8764 | 3,2667 |
| playwright | ram-heavy | 3,4214 | 113,4065 | 36,3264 | 325,9507 | 728,7819 | 3,4511 |
| cypress | baseline | 13,8553 | 143,7743 | 39,6870 | 957,4314 | 1333,6548 | 18,2570 |
| cypress | ui-heavy | 14,4136 | 145,0439 | 37,3141 | 989,7820 | 1342,5612 | 19,4522 |
| cypress | cpu-heavy | 14,1430 | 145,6246 | 37,7959 | 982,9772 | 1341,8803 | 19,0844 |
| cypress | ram-heavy | 14,2869 | 146,2134 | 38,4326 | 985,3780 | 1349,6941 | 19,4261 |

## ?statistiksel Kar??la?t?rma
| Profile | Metric | Mann-Whitney U | Cliff's delta | Welch t | Welch df | Cohen's d |
|---|---|---:|---:|---:|---:|---:|
| baseline | S?re (sn) | 0,0000 | -1,0000 | -35,1841 | 100,7116 | -4,9758 |
| baseline | Ortalama CPU (%) | 100,0000 | -0,9800 | -30,4388 | 155,9784 | -4,3047 |
| baseline | Ortalama sistem CPU (%) | 4554,0000 | -0,0892 | 0,2328 | 139,4277 | 0,0329 |
| baseline | Ortalama bellek (MB) | 0,0000 | -1,0000 | -197,4870 | 127,0057 | -27,9289 |
| baseline | Tepe bellek (MB) | 0,0000 | -1,0000 | -326,3103 | 146,3691 | -46,1472 |
| baseline | CPU s?resi (sn) | 0,0000 | -1,0000 | -200,9233 | 141,2996 | -28,4148 |
| ui-heavy | S?re (sn) | 0,0000 | -1,0000 | -488,2467 | 197,3907 | -69,0485 |
| ui-heavy | Ortalama CPU (%) | 0,0000 | -1,0000 | -46,4560 | 147,5128 | -6,5699 |
| ui-heavy | Ortalama sistem CPU (%) | 4394,0000 | -0,1212 | 0,6119 | 116,0917 | 0,0865 |
| ui-heavy | Ortalama bellek (MB) | 0,0000 | -1,0000 | -540,0594 | 153,3856 | -76,3759 |
| ui-heavy | Tepe bellek (MB) | 0,0000 | -1,0000 | -297,6416 | 146,8614 | -42,0929 |
| ui-heavy | CPU s?resi (sn) | 0,0000 | -1,0000 | -321,1217 | 146,2280 | -45,4135 |
| cpu-heavy | S?re (sn) | 0,0000 | -1,0000 | -571,5275 | 195,7102 | -80,8262 |
| cpu-heavy | Ortalama CPU (%) | 0,0000 | -1,0000 | -49,7756 | 156,8087 | -7,0393 |
| cpu-heavy | Ortalama sistem CPU (%) | 2135,5000 | -0,5729 | -6,2778 | 123,7413 | -0,8878 |
| cpu-heavy | Ortalama bellek (MB) | 0,0000 | -1,0000 | -521,2417 | 144,9551 | -73,7147 |
| cpu-heavy | Tepe bellek (MB) | 0,0000 | -1,0000 | -356,2426 | 187,3988 | -50,3803 |
| cpu-heavy | CPU s?resi (sn) | 0,0000 | -1,0000 | -313,5617 | 140,7575 | -44,3443 |
| ram-heavy | S?re (sn) | 0,0000 | -1,0000 | -494,7350 | 180,1824 | -69,9661 |
| ram-heavy | Ortalama CPU (%) | 0,0000 | -1,0000 | -48,1919 | 188,5043 | -6,8154 |
| ram-heavy | Ortalama sistem CPU (%) | 3090,0000 | -0,3820 | -4,2237 | 122,8948 | -0,5973 |
| ram-heavy | Ortalama bellek (MB) | 0,0000 | -1,0000 | -615,5941 | 178,2544 | -87,0582 |
| ram-heavy | Tepe bellek (MB) | 0,0000 | -1,0000 | -275,3290 | 170,9615 | -38,9374 |
| ram-heavy | CPU s?resi (sn) | 0,0000 | -1,0000 | -244,5419 | 116,8922 | -34,5835 |

## ??kt? Dosyalar?
- `results/{tool}/{profile}_benchmark_100.csv`: ham profil ?l??mleri
- `results/summaries/profile_metric_summary.csv`: tool/profile/metric bazl? genel ?zet
- `results/summaries/profile_comparison_stats.csv`: profil bazl? kar??la?t?rma istatistikleri
- `results/graphs/`: profil ve metrik bazl? kar??la?t?rma grafikleri

## Not
Tablolar virg?ll? ondal?k bi?ime d?n??t?r?lmeye uygun olacak ?ekilde raporlanm??t?r; ham CSV dosyalar? nokta ondal?kla saklanm??t?r.