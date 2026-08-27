# Voynich Notation Lab — Nihai araştırma sentezi

## Sonuç

Bu çalışma Voynich Elyazması'nı çözdüğünü iddia etmez. Bir hafta boyunca modern hesaplama gücü,
pozitif kontroller, bağımsız transkripsiyonlar ve önceden dondurulmuş testlerle çok sayıda klasik
açıklama sınandı. Ortaya çıkan en güçlü çalışma hipotezi şudur:

> Voynich yüzeyi sıradan bir dil veya klasik şifre değildir. Batı/Latin yazı geleneğinin görünümünü
> ve el hareketi ritmini kullanan, kişisel, kayıplı ve görsel-hatırlatıcı bir notasyon olabilir.

Yazar zihnindeki sözcük, ses, ritim veya kavramları eksiksiz kodlamak yerine kendisine yeterli
gelecek görsel çağrıştırıcılarla kaydetmiş olabilir. Resimler, sayfa konumu, paragraf biçimi ve
kişisel hafıza eksik bilgiyi tamamlamış olabilir. Bu nedenle metin yazarı için kolay okunabilirken,
dışarıdan tek bir anahtarla geri döndürülemeyebilir.

## Bizi buraya getiren ana deneyler

- Dört dilde doğrudan sınırlı eşleme, genel dil benzerliği üretti fakat gerçek sözcük/cümle
  sırasını geri getirmedi; pozitif kontroller dili güçlü biçimde geri kazandı.
- Basit procedural üretici Voynich yüzeyinin yalnız küçük bir bölümünü açıklayabildi.
- Bilinen Latinceyi ağır kısaltma ve satır-duyarlı gösterimden geçirmek Voynich benzeri yerel yapı
  üretti; bu yüzden yerellik dil ile üretimi ayıramadı.
- Exact-token tekrarları sayfa ve satır tahsisini gösterdi; satır envanteri sabitlenince güvenilir
  sözcük sırası sinyali kalmadı.
- Residual-capacity ve binary latent-state deneyleri geniş içerik hipotezlerini sıralamadı.
- Aynı Validation kümesinin tekrar kullanılması nedeniyle sınırsız model üretimi durduruldu.
- Süslü/yüksek başlangıçlar paragraf başlarında yaklaşık `%81–83`, diğer satırlarda `%8,5–8,6`
  oranında görüldü: paragraf tasarımı gerçekti.
- Zorunlu ve son harfe göre biçim değiştiren bir nokta modeli gerçek veride rastlantıya yakın
  kaldı; aynı cihaz sentetik noktayı yaklaşık `AUC 0,999` ile yakaladı.
- Sayfalar uzaklaştırıldığında Batı elyazısı hissi korundu; aynalanmış görüntü sözcük dokusunu
  korurken başlangıç ve okuma yönü ritmini bozdu. Tanınabilir Latince sözcük dizisi çıkmadı.

## Ne söyleyebiliriz?

- Yüzey bağımsız rastgele işaretlerden oluşmuyor; görsel ve yerleşimsel tasarım var.
- Test edilen temsil altında sıradan doğal-dil sırası veya klasik şifre anahtarı geri kazanılmadı.
- Paragraflar son noktadan çok boşluk, satır bitişi ve süslü başlangıçla ayrılıyor.
- Notasyon, yazarın zihnindeki gerçek dilin “kelime kelime resmi” olabilir.
- Gizli zihinsel dil Latince olmak zorunda değil; görünüm Latin yazı geleneğinden etkilenmiş olabilir.

## Ne söyleyemeyiz?

- Metin kesinlikle anlamsızdır.
- Metin çevrilmiştir veya çözülmüştür.
- Yazarın kimliği, tanısı, konuşma yeteneği veya amacı bilinmektedir.
- Belirli bir Voynich işaretinin sesi veya anlamı bulunmuştur.
- Görsel notasyon ile yapılandırılmış pseudo-yazı henüz kesin olarak ayrılmıştır.

## Son ayrım

Artık ana soru “hangi dil?” değildir:

1. Aynı resim/kavram uzak sayfalarda aynı görsel aileleri doğuruyorsa anlamlı kişisel notasyon;
2. benzerlik yalnız hemen önceki şekiller ve satırda kalan alanla açıklanıyorsa yapılandırılmış
   pseudo-yazı.

Yeni testler yalnız bu iki mekanizmayı önceden belirlenmiş, görsel ve kör kontrollerle ayırmalıdır.
