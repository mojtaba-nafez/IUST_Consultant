from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView
from channel.models import Channel, Subscription
from User.models import ConsultantProfile, UserProfile
from message.models import *
from django.core.files.base import File
from rest_framework.authtoken.models import Token
import os


class InsertFakeData(APIView):
    def get(self, request, format=None):
        try:

            # consultant=ConsultantProfile.objects.create(username="testttttt",user_type='Immigration', phone_number="09185676125", first_name="hosseiniiiiii", last_name="masoudiiiiiii", email="testtttttt@gmailcom",password='fdfddfxcsd', certificate="111")
            # channel=Channel.objects.create(name="chchchchc",description= "immegrate to Germany-------", invite_link='Immigrate-Germany-------------', consultant=consultant)
            # user = UserProfile.objects.create(username="ffffffffffff", email="ffffffffff@gmail.com", password="ffffffff", phone_number="09178125538",first_name="fffffff", last_name="fffff")
            # Subscription.objects.create(channel=channel, user=user)
            # print('user '+ user.username+' subscribe to channel '+ channel.name )

            ##   Normal User info:
            user_user_name = ['username0', 'username1', 'username2', 'username3', 'username4', 'username5', 'username6',
                              'username7', 'username8', 'username9', 'username10', 'username11', 'username12',
                              'username13', 'username14', 'username15', 'username16', 'username17', 'username18',
                              'username19', 'username20', 'username21', 'username22', 'username23', 'username24',
                              'username25', 'username26', 'username27', 'username28', 'username29', 'username30',
                              'username31', 'username32', 'username33', 'username34', 'username35', 'username36',
                              'username37', 'username38', 'username39']
            user_email = ['user0@gmail.com', 'user1@gmail.com', 'user2@gmail.com', 'user3@gmail.com', 'user4@gmail.com',
                          'user5@gmail.com', 'user6@gmail.com', 'user7@gmail.com', 'user8@gmail.com', 'user9@gmail.com',
                          'user10@gmail.com', 'user11@gmail.com', 'user12@gmail.com', 'user13@gmail.com',
                          'user14@gmail.com', 'user15@gmail.com', 'user16@gmail.com', 'user17@gmail.com',
                          'user18@gmail.com', 'user19@gmail.com', 'user20@gmail.com', 'user21@gmail.com',
                          'user22@gmail.com', 'user23@gmail.com', 'user24@gmail.com', 'user25@gmail.com',
                          'user26@gmail.com', 'user27@gmail.com', 'user28@gmail.com', 'user29@gmail.com',
                          'user30@gmail.com', 'user31@gmail.com', 'user32@gmail.com', 'user33@gmail.com',
                          'user34@gmail.com', 'user35@gmail.com', 'user36@gmail.com', 'user37@gmail.com',
                          'user38@gmail.com', 'user39@gmail.com']
            user_phone_number = ['09010000000', '09010000001', '09010000003', '09010000006', '09010000010',
                                 '09010000015', '09010000021', '09010000028', '09010000036', '09010000045',
                                 '09010000055', '09010000066', '09010000078', '09010000091', '09010000105',
                                 '09010000120', '09010000136', '09010000153', '09010000171', '09010000190',
                                 '09010000210', '09010000231', '09010000253', '09010000276', '09010000300',
                                 '09010000325', '09010000351', '09010000378', '09010000406', '09010000435',
                                 '09010000465', '09010000496', '09010000528', '09010000561', '09010000595',
                                 '09010000630', '09010000666', '09010000703', '09010000741', '09010000780']
            user_first_name = ['علی', 'احمد', 'رضا', 'بیژن', 'کوروش', 'بنیامین', 'کیومرث', 'علیرضا', 'غلام', 'محمد',
                               'مهدی', 'عرفان', 'کریم', 'بهروز', 'بهنام', 'صادق', 'باقر', 'هادی', 'حمید', 'اصغر',
                               'آرمین', 'امین', 'احسان', 'فرزاد', 'گرشا', 'حامد', 'حجت', 'آرش', 'میثم', 'محسن', 'احسان',
                               'امید', 'راغب', 'رضا', 'سینا', 'سهیل', 'حسین', 'سعید', 'رهام', 'امیر']
            user_last_name = ['علیان', 'احمدی', 'کرمی', 'ایرانی', 'افشاری', 'نظری', 'سهرابی', 'نیازی', 'حسنی', 'محمدی',
                              'مهدوی', 'کریمی', 'مصطفوی', 'بهرامی', 'نیکپور', 'موسوی', 'رضایی', 'هدایتی', 'صبوری',
                              'جعفری', 'زندی', 'قبادی', 'کرمیان', 'فرزینی', 'رضاییان', 'همایونی', 'اشرفی', 'مسیحی',
                              'ابراهیمی', 'احسانی', 'محسنی', 'حاجعلی', 'امیدی', 'بهرامی', 'درخشان', 'رحیمی', 'دینی',
                              'طلیسچی', 'پرهامی', 'رسولی']
            user_password = ['123456', '123456', '123456', '123456', '123456', '123456', '123456', '123456', '123456',
                             '123456', '123456', '123456', '123456', '123456', '123456', '123456', '123456', '123456',
                             '123456', '123456', '123456', '123456', '123456', '123456', '123456', '123456', '123456',
                             '123456', '123456', '123456', '123456', '123456', '123456', '123456', '123456', '123456',
                             '123456', '123456', '123456', '123456']

            # Consultant Info + his channel
            # consultant_type = ['Lawyer', 'medical', 'EntranceExam'] #  'Psychology', 'Immigration', 'AcademicAdvice'
            consultant_type = ['Lawyer', 'Lawyer', 'Lawyer', 'Lawyer', 'Lawyer', 'Lawyer', 'Lawyer', 'Lawyer', 'Lawyer',
                               'Lawyer', 'medical', 'medical', 'medical', 'medical', 'medical', 'medical', 'medical',
                               'medical', 'medical', 'medical', 'EntranceExam', 'EntranceExam', 'EntranceExam',
                               'EntranceExam', 'EntranceExam', 'EntranceExam', 'EntranceExam', 'EntranceExam',
                               'EntranceExam', 'EntranceExam', 'Psychology', 'Psychology', 'Psychology', 'Psychology',
                               'Psychology', 'Psychology', 'Psychology', 'Psychology', 'Psychology', 'Psychology',
                               'Immigration', 'Immigration', 'Immigration', 'Immigration', 'Immigration', 'Immigration',
                               'Immigration', 'Immigration', 'Immigration', 'Immigration', 'AcademicAdvice',
                               'AcademicAdvice', 'AcademicAdvice', 'AcademicAdvice', 'AcademicAdvice', 'AcademicAdvice',
                               'AcademicAdvice', 'AcademicAdvice', 'AcademicAdvice', 'AcademicAdvice']
            consultant_username = ['username40', 'username41', 'username42', 'username43', 'username44', 'username45',
                                   'username46', 'username47', 'username48', 'username49', 'username50', 'username51',
                                   'username52', 'username53', 'username54', 'username55', 'username56', 'username57',
                                   'username58', 'username59', 'username60', 'username61', 'username62', 'username63',
                                   'username64', 'username65', 'username66', 'username67', 'username68', 'username69',
                                   'username70', 'username71', 'username72', 'username73', 'username74', 'username75',
                                   'username76', 'username77', 'username78', 'username79', 'username80', 'username81',
                                   'username82', 'username83', 'username84', 'username85', 'username86', 'username87',
                                   'username88', 'username89', 'username90', 'username91', 'username92', 'username93',
                                   'username94', 'username95', 'username96', 'username97', 'username98', 'username99']
            consultant_phone_number = ['09010000820', '09010000861', '09010000903', '09010000946', '09010000990',
                                       '09010001035', '09010001081', '09010001128', '09010001176', '09010001225',
                                       '09010001275', '09010001326', '09010001378', '09010001431', '09010001485',
                                       '09010001540', '09010001596', '09010001653', '09010001711', '09010001770',
                                       '09010001830', '09010001891', '09010001953', '09010002016', '09010002080',
                                       '09010002145', '09010002211', '09010002278', '09010002346', '09010002415',
                                       '09010002485', '09010002556', '09010002628', '09010002701', '09010002775',
                                       '09010002850', '09010002926', '09010003003', '09010003081', '09010003160',
                                       '09010003240', '09010003321', '09010003403', '09010003486', '09010003570',
                                       '09010003655', '09010003741', '09010003828', '09010003916', '09010004005',
                                       '09010004095', '09010004186', '09010004278', '09010004371', '09010004465',
                                       '09010004560', '09010004656', '09010004753', '09010004851', '09010004950']
            consultant_email = ['user40@gmail.com', 'user41@gmail.com', 'user42@gmail.com', 'user43@gmail.com',
                                'user44@gmail.com', 'user45@gmail.com', 'user46@gmail.com', 'user47@gmail.com',
                                'user48@gmail.com', 'user49@gmail.com', 'user50@gmail.com', 'user51@gmail.com',
                                'user52@gmail.com', 'user53@gmail.com', 'user54@gmail.com', 'user55@gmail.com',
                                'user56@gmail.com', 'user57@gmail.com', 'user58@gmail.com', 'user59@gmail.com',
                                'user60@gmail.com', 'user61@gmail.com', 'user62@gmail.com', 'user63@gmail.com',
                                'user64@gmail.com', 'user65@gmail.com', 'user66@gmail.com', 'user67@gmail.com',
                                'user68@gmail.com', 'user69@gmail.com', 'user70@gmail.com', 'user71@gmail.com',
                                'user72@gmail.com', 'user73@gmail.com', 'user74@gmail.com', 'user75@gmail.com',
                                'user76@gmail.com', 'user77@gmail.com', 'user78@gmail.com', 'user79@gmail.com',
                                'user80@gmail.com', 'user81@gmail.com', 'user82@gmail.com', 'user83@gmail.com',
                                'user84@gmail.com', 'user85@gmail.com', 'user86@gmail.com', 'user87@gmail.com',
                                'user88@gmail.com', 'user89@gmail.com', 'user90@gmail.com', 'user91@gmail.com',
                                'user92@gmail.com', 'user93@gmail.com', 'user94@gmail.com', 'user95@gmail.com',
                                'user96@gmail.com', 'user97@gmail.com', 'user98@gmail.com', 'user99@gmail.com']
            consultant_first_name = ['حسن', 'عباس', 'حسین', 'محمد', 'مجید', 'ابراهیم', 'بهمن', 'علی', 'سجاد', 'رضا',
                                     'عبدالله', 'مصطفی', 'محمدجواد', 'سعید', 'مهدی', 'صادق', 'میلاد', 'امیر', 'رسول',
                                     'امیرمحمد', 'حمیدرضا', 'طاها', 'ابوالفضل', 'مجتبی', 'خلیل', 'ناصر', 'پویا', 'یوسف',
                                     'بهادر', 'عباس', 'نیما', 'هومن', 'داوود', 'اسماعیل', 'فیروز', 'مرتضی', 'بهزاد',
                                     'پژمان', 'سام', 'محسن', 'هاشم', 'اسماعیل', 'علی', 'حسین', 'رضا', 'اکبر', 'محمدرضا',
                                     'فرشاد', 'عرفان', 'خسرو', 'علیرضا', 'علی', 'فرهاد', 'عباس', 'بابک', 'سهراب',
                                     'محمود', 'منصور', 'جمال', 'مسعود']
            consultant_last_name = ['احمدی', 'بوعذار', 'رحیمی', 'رحمانی', 'علیزاده', 'هادیان', 'آذری', 'حسینی',
                                    'یزدانی', 'خوشمرام', 'ممغینی', 'غلامی', 'سلطانی', 'موسوی', 'طاهری', 'پناهی',
                                    'عبادی', 'نصرتی', 'جعفری', 'نادری', 'آذرباد', 'سعیدی', 'حیدری', 'جلیلی', 'حیرانی',
                                    'محبی', 'نوروزی', 'جهانی', 'بهمنش', 'رمضانی', 'افشار', 'ملکی', 'سوزمانی', 'خورشیدی',
                                    'هلالی', 'شاهرودی', 'امیری', 'درخشانی', 'جمشیدی', 'شیخی', 'هاشم گلی', 'قربانی',
                                    'غدیری', 'کربلایی', 'مشهدی', 'نجفی', 'ذبیحی', 'جوهری', 'صدر', 'شکیبی', 'زارعی',
                                    'امیری', 'رضوی', 'قاسمی', 'کتابی', 'سلیمی', 'روحی', 'کریمی', 'جباری', 'شهریاری']
            consultant_password = ['123456', '123456', '123456', '123456', '123456', '123456', '123456', '123456',
                                   '123456', '123456', '123456', '123456', '123456', '123456', '123456', '123456',
                                   '123456', '123456', '123456', '123456', '123456', '123456', '123456', '123456',
                                   '123456', '123456', '123456', '123456', '123456', '123456', '123456', '123456',
                                   '123456', '123456', '123456', '123456', '123456', '123456', '123456', '123456',
                                   '123456', '123456', '123456', '123456', '123456', '123456', '123456', '123456',
                                   '123456', '123456', '123456', '123456', '123456', '123456', '123456', '123456',
                                   '123456', '123456', '123456', '123456']
            invite_link = ['vakil0', 'vakil1', 'vakil2', 'vakil3', 'vakil4', 'vakil5', 'vakil6', 'vakil7', 'vakil8',
                           'vakil9', 'doctor10', 'doctor11', 'doctor12', 'doctor13', 'doctor14', 'doctor15', 'doctor16',
                           'doctor17', 'doctor18', 'doctor19', 'konkur20', 'konkur21', 'konkur22', 'konkur23',
                           'konkur24', 'konkur25', 'konkur26', 'konkur27', 'konkur28', 'konkur29', 'Psychology30',
                           'Psychology31', 'Psychology32', 'Psychology33', 'Psychology34', 'Psychology35',
                           'Psychology36', 'Psychology37', 'Psychology38', 'Psychology39', 'Immigration40',
                           'Immigration41', 'Immigration42', 'Immigration43', 'Immigration44', 'Immigration45',
                           'Immigration46', 'Immigration47', 'Immigration48', 'Immigration49', 'AcademicAdvice50',
                           'AcademicAdvice51', 'AcademicAdvice52', 'AcademicAdvice53', 'AcademicAdvice54',
                           'AcademicAdvice55', 'AcademicAdvice56', 'AcademicAdvice57', 'AcademicAdvice58',
                           'AcademicAdvice59']
            description = ['متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید',
                           'متنی برای پر کردن توضیحات کانال خودتون بعدا تغییر بدید']
            channel_name = ['وکیل', 'مشاوره وکالت', 'وکیل خانواده', 'وکیل پایه یک', 'وکیل دادگستری', 'مشاوره حقوقی',
                            'مشاوره حقیقی', 'حق و حقوق', 'اموزش قانون', 'گرفتن حق', 'دکتر سلام', 'دکتر چه طوری؟',
                            'دکتر خداحافظ', 'آموزش دکتری', 'مشاوره پزشکی', 'طب سنتی', 'طب صنعتی', 'آموزش کمک اولیه',
                            'درمان خانگی', 'نکات پزشکی', 'آموزش کنکور', 'کنکوری ها', 'نکات طلایی کنکور',
                            'نکات نقره ای کنکور', 'نکات برنزی کنکور', 'نکات', 'راه کنکور', 'برنامه ریزی کنکور',
                            'کنکورت رو قورت بده', 'فرمول طلایی', 'دکتر نیما افشار', 'روانشناسی با ملکی', 'روانشناسی',
                            'رواننشناسی', 'درمان روان پریشی', 'درمان پارانوئید', 'روان آرام', 'اعتماد به نفس',
                            'نکات روانی', 'آموزش روانشناسی', 'مهاجرت تحصیلی', 'مهاجرت تفریحی', 'مهاجرت کاری',
                            'مهاجرت شغلی', 'مهاجرت پرندگان', 'کجا', 'کی', 'چی', 'چه جوری', 'نه', 'مشاوره تحصیلی',
                            'رشته دانشگاهی', 'رشته دبیرستان', 'رشته آشی', 'یازدهمی ها', 'معرفی دانشگاه ها',
                            'مشاوره درسی', 'دیتا بیس', 'رو پاک نکنید', 'خسته شدم']

            # message_text = ["welcome.", 'injoy the channel content.', 'glad to meet you']
            message_text = ['welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you',
                            'welcome injoy the channel content., glad to meet you']
            users = []
            for i in range(len(user_user_name)):
                try:
                    user = UserProfile.objects.create(username=user_user_name[i], email=user_email[i],
                                                      password=user_password[i], phone_number=user_phone_number[i],
                                                      first_name=user_first_name[i], last_name=user_last_name[i], avatar=File(open(os.path.dirname(__file__)+'/files/user/'+ str((i+1)) +'.jpeg', 'rb')))
                    Token.objects.create(user=user)
                    users.append(user)
                    print('user ' + user_user_name[i] + ' created')
                except:
                    pass

            consultants = []
            channels = []
            for j in range(len(consultant_username)):
                try:
                    consultant = ConsultantProfile.objects.create(username=consultant_username[j],
                                                                  user_type=consultant_type[j],
                                                                  phone_number=consultant_phone_number[j],
                                                                  first_name=consultant_first_name[j],
                                                                  last_name=consultant_last_name[j],
                                                                  email=consultant_email[j],
                                                                  password=consultant_password[j], certificate="111", avatar=File(open(os.path.dirname(__file__)+'/files/user/'+ str(j+1) +'.jpeg', 'rb')))
                    Token.objects.create(user=consultant)
                    consultants.append(consultant)
                    print('consultant ' + consultant_username[j] + ' created')
                    channel = Channel.objects.create(name=channel_name[j], description=description[j],
                                                     invite_link=invite_link[j], consultant=consultant, avatar=File(open(os.path.dirname(__file__)+'/files/channel_consultant/'+ str(j+1) +'.png', 'rb')))
                    print('channel ' + channel_name[j] + ' created')
                    channels.append(channel)
                    for k in range(len(message_text)):
                        try:
                            print("i wat to add : " + message_text[k])
                            ChannelMessage.objects.create(text=message_text[k], message_type='text', channel=channel,
                                                          creator=consultant)
                            print('message ' + message_text[k] + ' added to channel' + channel.name)
                        except:
                            print("can not add : " + message_text[k] + ' to channel ',
                                  channel.name + ' consultant: ' + consultant.username)
                    for i in range(len(users)):
                        try:
                            Subscription.objects.create(channel=channel, user=users[i])
                            print('user ' + users[i].username + ' subscribe to channel ' + channel.name)
                        except:
                            print("try")
                except:
                    pass
            return Response(data={"status": "ok"}, status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
