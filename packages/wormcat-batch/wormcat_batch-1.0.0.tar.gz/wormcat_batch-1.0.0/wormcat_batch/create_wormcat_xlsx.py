import pandas as pd

# Create summary category column
def create_category_summary(data, category_name):
    category = data[category_name].value_counts()
    category = pd.DataFrame({category_name: category.index, 'Count': category.values})
    category = category.sort_values(by=[category_name])
    return category


def process_category_file_row(row,sheet):
    file_name =  row['file']
    label_category = "Category {}".format(row['category'])
    label_PValue = "{}_PValue".format(row['label'])
    label_RGS = "{}_RGS".format(row['label'])

    cat_results = pd.read_csv(file_name)
    cat_results.rename(columns={'Category': label_category,'RGS':label_RGS,'PValue':label_PValue}, inplace=True)
    cat_results.drop('Unnamed: 0', axis=1, inplace=True)
    cat_results.drop('AC', axis=1, inplace=True)

    sheet = pd.merge(sheet, cat_results, on=label_category, how='outer')
    sheet[label_PValue] = sheet[label_PValue].apply(significant)
    sheet[label_RGS] = sheet[label_RGS].apply(lambda x: x if x > 0 else 0)
    return sheet


# Test if the P Value is significant
def significant(x):
    ret_val = 'NV'
    if x < 0.05:
        ret_val = x
    elif x >= 0.05:
        ret_val = 'NS'
    return ret_val


def process_category_files(files_to_process, annotation_file, out_data_xlsx):
    data = pd.read_csv(annotation_file)
    writer = pd.ExcelWriter("{}".format(out_data_xlsx), engine='xlsxwriter')

    #files_to_process = pd.read_csv("{}/files_to_process.csv".format(base_dir))

    sheets = files_to_process['sheet'].unique()

    for sheet_label in sheets:
        cat_files = files_to_process[files_to_process['sheet'] == sheet_label]
        label_category = "Category {}".format(cat_files['category'].iloc[0])
        category_sheet = create_category_summary(data, label_category)
        for index, row in cat_files.iterrows():
            category_sheet = process_category_file_row(row, category_sheet)

        category_sheet.to_excel(writer, sheet_name=sheet_label, index=False)

    writer.save()

