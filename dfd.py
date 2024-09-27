import 'dart:io';
import 'package:admin/utility/snack_bar_helper.dart';

import '../../../services/http_services.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart' hide Category;
import 'package:get/get.dart';
import 'package:image_picker/image_picker.dart';
import '../../../core/data/data_provider.dart';
import '../../../models/category.dart';

class CategoryProvider extends ChangeNotifier {
  HttpService service = HttpService();
  final DataProvider _dataProvider;
  final addCategoryFormKey = GlobalKey<FormState>();
  TextEditingController categoryNameCtrl = TextEditingController();
  Category? categoryForUpdate;



  File? selectedImage;
  XFile? imgXFile;


  CategoryProvider(this._dataProvider);

  addCategory() async {
    try {
      if(selectedImange == null){
        SnackBarHelper.showErrorSnackBar('please choice a image');
        return;
      }
      map<String, dynamic> formDataMap = {
        'name': categoryNameCtrl.text,
        'image': 'no_data',
      };

      final FormData from = await createFormData(imgXFile: imgXFile, formData: formDataMap);

      final response = await service.additem(endpointUrl: 'categories', itemdata: from);
      if (response.isOk) {
        ApiResponse apiresponse = ApiResponse.fromJason(response.body, null);
        if (apiresponse.success == true) {
          clearFields();
          SnackBarHelper.showSuccessSnackBar('${ApiResponse.message}');
          log('category added');
        } else {
          SnackBarHelper.showErrorSnackBar('Failed to add category: ${apiresponse.message}');
        }
      } else {
        SnackBarHelper.showErrorSnackBar('Error ${response.body?{'message'}}') ?? response.statusText}');
    }
  } catch (e) {
  print(e);
  SnackBarHelper.showErrorSnackBar('An Error occurred: $e');
  rethrow;
  }
}


void pickImage() async {
  final ImagePicker picker = ImagePicker();
  final XFile? image = await picker.pickImage(source: ImageSource.gallery);
  if (image != null) {
    selectedImage = File(image.path);
    imgXFile = image;
    notifyListeners();
  }
}
//? to create form data for sending image with body
Future<FormData> createFormData({required XFile? imgXFile, required Map<String, dynamic> formData}) async {
  if (imgXFile != null) {
    MultipartFile multipartFile;
    if (kIsWeb) {
      String fileName = imgXFile.name;
      Uint8List byteImg = await imgXFile.readAsBytes();
      multipartFile = MultipartFile(byteImg, filename: fileName);
    } else {
      String fileName = imgXFile.path.split('/').last;
      multipartFile = MultipartFile(imgXFile.path, filename: fileName);
    }
    formData['img'] = multipartFile;
  }
  final FormData form = FormData(formData);
  return form;
}

//? set data for update on editing
setDataForUpdateCategory(Category? category) {
  if (category != null) {
    clearFields();
    categoryForUpdate = category;
    categoryNameCtrl.text = category.name ?? '';
  } else {
    clearFields();
  }
}

//? to clear text field and images after adding or update category
clearFields() {
  categoryNameCtrl.clear();
  selectedImage = null;
  imgXFile = null;
  categoryForUpdate = null;
}
}
